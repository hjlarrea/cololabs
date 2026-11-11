"""Check the domain and indexing boundaries of an actual Pelican build."""
import sys
from pathlib import Path


def check(directory, mode):
    root = Path(directory)
    index = (root / 'index.html').read_text()
    assert (root / 'theme/css/style.css').is_file(), 'Missing theme assets'
    if mode == 'preview':
        assert not (root / 'CNAME').exists(), 'Production CNAME leaked into preview'
        assert not (root / 'feeds').exists(), 'Feeds must not be generated in preview'
        assert 'Disallow: /' in (root / 'robots.txt').read_text()
        for html in root.rglob('*.html'):
            text = html.read_text()
            assert 'noindex, nofollow, noarchive' in text, f'Missing noindex: {html}'
            assert 'Preview — unpublished review copy.' in text, f'Missing banner: {html}'
            assert 'https://cololabs.com.ar' not in text, f'Production URL in {html}'
    else:
        assert (root / 'CNAME').read_text().strip() == 'cololabs.com.ar'
        assert (root / 'feeds/all.atom.xml').is_file()
        assert 'noindex, nofollow, noarchive' not in index
        assert 'Preview — unpublished review copy.' not in index
        assert 'https://cololabs.com.ar/theme/css/style.css' in index
    print(f'{mode} build checks passed: {root}')


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[2] not in ('preview', 'production'):
        sys.exit('Usage: python scripts/check_build.py OUTPUT_DIRECTORY preview|production')
    check(*sys.argv[1:])
