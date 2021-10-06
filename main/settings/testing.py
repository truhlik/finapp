from .base import *

ALLOW_ROBOTS = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

try:
    from .local import *
except ImportError:
    pass
