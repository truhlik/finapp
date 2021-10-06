from .testing import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'finapp',
        'USER': 'finapp',
        'PASSWORD': 'finapp',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}
