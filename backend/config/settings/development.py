from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*.ngrok.io']

INSTALLED_APPS += [
    'django_extensions',
    'drf_yasg',
]

DATABASES['default']['NAME'] = 'library_db'

CELERY_TASK_ALWAYS_EAGER = True

if 'loggers' in LOGGING:
    LOGGING['loggers'].update({
        'django': {'level': 'DEBUG'},
        'apps': {'level': 'DEBUG'},
    })
