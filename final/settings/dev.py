from .base import *

SECRET_KEY = env('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'second_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'second_db.sqlite3',
    }
}

DATABASE_ROUTERS = ['final.router.SecondAppRouter']
# DATABASES = {
#     'default': env.db()
# }
