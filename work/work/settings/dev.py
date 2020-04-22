import json

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')
DEBUG = os.getenv('DEBUG', True)

DATABASES = {
    'default': {
        'NAME': os.getenv('DATABASE_NAME'),
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.getenv('DATABASE_USERNAME'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD')
    },
}
