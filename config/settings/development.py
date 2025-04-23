from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True