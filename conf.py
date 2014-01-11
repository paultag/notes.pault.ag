# -*- coding: utf-8 -*-
from __future__ import unicode_literals

AUTHOR = 'Paul Tagliamonte'
SITENAME = "Ceci n'est pas une -EPIPE"
SITETAG = "Life as a F/OSS Zealot, Debianite, Pythonista and Lisper"
SITEURL = 'http://notes.pault.ag'
SITEURL = 'http://localhost/blog'
TIMEZONE = "America/New_York"
THEME = "epipe"

GITHUB_URL = 'git://github.com/paultag/notes.pault.ag.git'
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True

DEFAULT_PAGINATION = 30
DEFAULT_DATE = (2013, 3, 2, 14, 1, 1)

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

MARKUP = ('rst', 'md', 'html')

LINKS = (('Blog', 'http://blog.pault.ag'),)

SOCIAL = (('twitter', 'http://twitter.com/paultag'),
          ('google-plus', 'http://gplus.to/paultag'),
          ('music', 'http://rdio.com/people/paultag'),
          ('github', 'http://git.io/paultag'),)

# global metadata to all the contents
DEFAULT_METADATA = ()  #(('yeah', 'it is'),)

# static paths will be copied under the same name
STATIC_PATHS = ["../static", ]

# A list of files to copy from the source to the destination
# FILES_TO_COPY = (('static/notes.png', 'notes.png'),)

# custom page generated with a jinja2 template
TEMPLATE_PAGES = {}  # 'pages/jinja2_template.html': 'jinja2_template.html'}

ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = "{slug}/index.html"
