from .base import *

DEBUG = True
DEBUG_TOOLBAR = True
ALLOW_ROBOTS = False
COMPRESS_ENABLED = False

INTERNAL_IPS = ['127.0.0.1']
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
INSTALLED_APPS += [
    'debug_toolbar',
]
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

try:
    from .local import *
except ImportError:
    pass
