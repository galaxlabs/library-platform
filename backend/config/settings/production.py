import os

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '72.60.118.195', 'library.digigalaxy.cloud']

# SSL redirect handled by Nginx and forwarded headers.
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

DATABASES['default']['ATOMIC_REQUESTS'] = True
