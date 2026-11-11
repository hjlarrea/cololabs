"""Isolated preview settings; never use the production custom domain."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pelicanconf import *

SITEURL = os.environ.get('PREVIEW_SITEURL', 'https://preview.cololabs.com.ar').rstrip('/')
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
PREVIEW = True
PREVIEW_COMMIT = os.environ.get('PREVIEW_COMMIT', 'local build')
SITELOGO = SITEURL + '/images/darkLogo.png'
USER_LOGO_URL = SITELOGO
FAVICON = SITEURL + '/images/favicon.ico'
MENUITEMS = (('Home', SITEURL + '/'),)
STATIC_PATHS = ['images', 'extra/.nojekyll', 'extra/preview-robots.txt']
EXTRA_PATH_METADATA = {
    'extra/.nojekyll': {'path': '.nojekyll'},
    'extra/preview-robots.txt': {'path': 'robots.txt'},
}
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
GOOGLE_ANALYTICS = None
DISQUS_SITENAME = None
