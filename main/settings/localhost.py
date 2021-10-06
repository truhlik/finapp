from .base import *

DEBUG = True
DEBUG_TOOLBAR = True
ALLOW_ROBOTS = True

INTERNAL_IPS = ['127.0.0.1']
AXES_IP_WHITELIST = INTERNAL_IPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
INSTALLED_APPS += [
    'debug_toolbar',
]
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# from local.py
config = AutoConfig(os.environ.get('DJANGO_CONFIG_ENV_DIR'))
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(config('PROJECT_HOME_DIR', ''), 'tmp/emails/')
os.makedirs(EMAIL_FILE_PATH, exist_ok=True)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'main.libraries.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'SEARCH_PARAM': 'q',
}

GOOGLE_MAPS_API_KEY = 'GCsJ3G9DGFEPQkl93F6IDLkiJ74='
AUTH_PASSWORD_VALIDATORS = []

try:
    from .local import *
except ImportError:
    pass
