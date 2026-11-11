"""Human and OpenClaw entry points for proposing articles; no production deployment."""
import argparse
import json
import re
import subprocess
import sys
import urllib.request

PRODUCTION = 'hjlarrea/cololabs'
PREVIEW = 'hjlarrea/cololabs-preview'
PREVIEW_URL = 'https://preview.cololabs.com.ar'


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def require(condition, message):
    if not condition:
        sys.exit(message)


def fetch(repo, branch):
    run('git', 'fetch', '--no-tags', f'https://github.com/{repo}.git',
        f'refs/heads/{branch}')
    return run('git', 'rev-parse', 'FETCH_HEAD')


def start(slug):
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug),
            'Use a lowercase slug containing words separated by hyphens.')
    require(not run('git', 'status', '--porcelain'), 'Commit or stash local changes first.')
    origin = run('git', 'remote', 'get-url', 'origin').removesuffix('.git')
    require(origin in (f'git@github.com:{PREVIEW}', f'https://github.com/{PREVIEW}'),
            f'Run start from a clone of {PREVIEW}; origin must point to the preview repository.')
    sha = fetch(PRODUCTION, 'main')
    run('git', 'switch', '-c', f'proposals/{slug}', sha)
    print(f'Created proposals/{slug} from production main ({sha}).')
    print('Write the article, commit it, then: git push -u origin HEAD')


def promote(branch, reviewed_sha):
    require(re.fullmatch(r'proposals/[a-z0-9]+(?:-[a-z0-9]+)*', branch),
            'Expected proposals/lowercase-article-slug.')
    require(re.fullmatch(r'[0-9a-f]{40}', reviewed_sha),
            'Supply the full 40-character commit shown in the deployed preview.')
    sha = fetch(PREVIEW, branch)
    require(sha == reviewed_sha, 'The proposal changed after review. Review its new preview first.')
    # Confirm that the live shared preview is the exact proposal being promoted.
    with urllib.request.urlopen(PREVIEW_URL + '/preview.json', timeout=20) as response:
        deployed = json.load(response)
    require(deployed.get('commit') == sha and deployed.get('branch') == branch
            and deployed.get('repository') == PREVIEW,
            'The live preview belongs to another commit/branch. Redeploy and review this proposal first.')
    base = fetch(PRODUCTION, 'main')
    ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', base, sha], check=False)
    require(ancestor.returncode == 0,
            'Production main has changed. Merge its latest main into the proposal, push, and review again.')
    changed = run('git', 'diff', '--name-only', '--no-renames', base, sha).splitlines()
    require(changed, 'This proposal contains no changes relative to production main.')
    unexpected = [p for p in changed if not p.startswith(('content/articles/', 'content/images/'))]
    require(not unexpected, 'Article promotion allows only content/articles/ and content/images/. '
            f'Review infrastructure changes separately: {unexpected}')
    head = 'review/' + branch.removeprefix('proposals/') + '-' + sha[:12]
    # Push a fixed commit, never a moving branch name or a force push.
    run('git', 'push', f'https://github.com/{PRODUCTION}.git', f'{sha}:refs/heads/{head}')
    existing = json.loads(run('gh', 'pr', 'list', '--repo', PRODUCTION, '--head', head,
                             '--base', 'main', '--json', 'url'))
    if existing:
        print(existing[0]['url'])
        return
    body = (f'Article proposed in https://github.com/{PREVIEW}/tree/{branch}.\n\n'
            f'Reviewed preview: {PREVIEW_URL}\n\nReviewed commit: `{sha}`\n\n'
            'This PR contains the exact reviewed commit. Merge it after editorial approval, '
            'then publish manually using the documented production procedure.\n')
    print(run('gh', 'pr', 'create', '--repo', PRODUCTION, '--base', 'main', '--head', head,
              '--title', 'Article: ' + branch.removeprefix('proposals/').replace('-', ' '),
              '--body', body))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    new = sub.add_parser('start', help='Start an article in a preview-repository clone')
    new.add_argument('slug')
    promotion = sub.add_parser('promote', help='Human only: open a production PR for a reviewed commit')
    promotion.add_argument('branch')
    promotion.add_argument('reviewed_sha')
    args = parser.parse_args()
    try:
        if args.command == 'start':
            start(args.slug)
        else:
            promote(args.branch, args.reviewed_sha)
    except (subprocess.CalledProcessError, OSError, ValueError) as error:
        sys.exit(f'Editorial command failed: {error}')


if __name__ == '__main__':
    main()
