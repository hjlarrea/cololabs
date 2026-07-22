AUTHOR = 'Hernan J. Larrea'
SITENAME = ''
SITEURL = ""

I18N_TEMPLATES_LANG = "en"

MAIN_MENU = True
SITELOGO = SITEURL + "/images/darkLogo.png"
FAVICON = SITEURL + "/images/favicon.ico"
ASSET_VERSION = '20260722-4'
PATH = "content"

TIMEZONE = 'America/Argentina/Buenos_Aires'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "themes/svbhack"
ROUND_USER_LOGO = False
USER_LOGO_URL = SITEURL + "/images/darkLogo.png"
ARTICLE_PATHS = ['articles']
STATIC_PATHS = ['images', 'extra/CNAME', 'extra/.nojekyll']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/.nojekyll': {'path': '.nojekyll'},
}
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = (
    ('Home', SITEURL + '/'),
)


# Blogroll
#LINKS = (
#    ("Pelican", "https://getpelican.com/"),
#    ("Python.org", "https://www.python.org/"),
#    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
#    ("You can modify those links in your config file", "#"),
#)

# Social widget
SOCIAL = (
    ("Larrea", "https://larrea.com.ar"),
    ("GitHub", "https://github.com/hjlarrea"),
    ("LinkedIn", "https://linkedin.com/in/hjlarrea"),
    ("YouTube","https://youtube.com/@cololabs")
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
