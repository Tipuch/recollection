import dj_database_url

from .settings import *

DEBUG = False

ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]

STATIC_ROOT = os.environ['STATIC_PATH']
STATIC_URL = os.environ['STATIC_URL']

MEDIA_ROOT = os.environ['MEDIA_PATH']
MEDIA_URL = os.environ['MEDIA_URL']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES['default'] = dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
