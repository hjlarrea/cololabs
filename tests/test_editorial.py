"""Exercise promotion against real Git history, without network or remote writes."""
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('editorial', Path(__file__).resolve().parents[1] / 'scripts/editorial.py')
editorial = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(editorial)


class EditorialTest(unittest.TestCase):
    def git(self, *args):
        return subprocess.check_output(['git', *args], text=True, stderr=subprocess.DEVNULL).strip()

    def commit(self, filename, content):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.git('add', filename)
        self.git('commit', '-m', 'fixture')
        return self.git('rev-parse', 'HEAD')

    def setUp(self):
        self.original_cwd = Path.cwd()
        self.directory = tempfile.TemporaryDirectory()
        os.chdir(self.directory.name)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.com')
        self.base = self.commit('README.md', 'Base\n')
        self.sha = self.commit('content/articles/article.md', 'Title: Article\n')
        self.branch = 'proposals/article'
        self.deployed_sha = self.sha
        self.remote_sha = self.sha
        self.remote_base = self.base
        self.calls = []
        self.original_run = editorial.run
        self.existing = []
        self.patches = [
            patch.object(editorial, 'fetch', side_effect=lambda repo, branch:
                         self.remote_sha if repo == editorial.PREVIEW else self.remote_base),
            patch.object(editorial.urllib.request, 'urlopen', side_effect=lambda *a, **kw:
                         io.BytesIO(json.dumps({'commit': self.deployed_sha, 'branch': self.branch,
                                                'repository': editorial.PREVIEW}).encode())),
            patch.object(editorial, 'run', side_effect=self.fake_run),
        ]
        for p in self.patches:
            p.start()

    def fake_run(self, *args):
        self.calls.append(args)
        if args[:2] == ('git', 'push'):
            return ''
        if args[:3] == ('gh', 'pr', 'list'):
            return json.dumps(self.existing)
        if args[:3] == ('gh', 'pr', 'create'):
            return 'https://github.com/hjlarrea/cololabs/pull/123'
        return self.original_run(*args)

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        os.chdir(self.original_cwd)
        self.directory.cleanup()

    def assert_no_push(self):
        self.assertFalse(any(call[:2] == ('git', 'push') for call in self.calls))

    def test_promotes_exact_reviewed_commit(self):
        editorial.promote(self.branch, self.sha)
        pushes = [call for call in self.calls if call[:2] == ('git', 'push')]
        self.assertEqual(pushes, [('git', 'push', 'https://github.com/hjlarrea/cololabs.git',
                                  f'{self.sha}:refs/heads/review/article-{self.sha[:12]}')])
        self.assertTrue(any(call[:3] == ('gh', 'pr', 'create') for call in self.calls))

    def test_rejects_proposal_changed_after_review(self):
        self.remote_sha = 'f' * 40
        with self.assertRaisesRegex(SystemExit, 'changed after review'):
            editorial.promote(self.branch, self.sha)
        self.assert_no_push()

    def test_rejects_live_preview_from_another_commit(self):
        self.deployed_sha = self.base
        with self.assertRaisesRegex(SystemExit, 'another commit/branch'):
            editorial.promote(self.branch, self.sha)
        self.assert_no_push()

    def test_rejects_infrastructure_changes(self):
        self.sha = self.commit('.github/workflows/changed.yml', 'changed\n')
        self.remote_sha = self.deployed_sha = self.sha
        with self.assertRaisesRegex(SystemExit, 'infrastructure changes separately'):
            editorial.promote(self.branch, self.sha)
        self.assert_no_push()

    def test_requires_latest_production_main(self):
        self.git('checkout', self.base)
        self.remote_base = self.commit('content/articles/other.md', 'Other article\n')
        with self.assertRaisesRegex(SystemExit, 'Production main has changed'):
            editorial.promote(self.branch, self.sha)
        self.assert_no_push()

    def test_reuses_existing_pr(self):
        self.existing = [{'url': 'https://github.com/hjlarrea/cololabs/pull/123'}]
        editorial.promote(self.branch, self.sha)
        self.assertFalse(any(call[:3] == ('gh', 'pr', 'create') for call in self.calls))

    def test_start_requires_preview_clone(self):
        self.git('remote', 'add', 'origin', 'https://github.com/hjlarrea/cololabs.git')
        with self.assertRaisesRegex(SystemExit, 'preview repository'):
            editorial.start('article')

    def test_start_creates_branch_from_production(self):
        self.git('remote', 'add', 'origin', 'https://github.com/hjlarrea/cololabs-preview.git')
        editorial.start('new-article')
        self.assertEqual(self.git('branch', '--show-current'), 'proposals/new-article')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)


if __name__ == '__main__':
    unittest.main()
