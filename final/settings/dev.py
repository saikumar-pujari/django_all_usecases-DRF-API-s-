from .base import *

SECRET_KEY = config('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
