import os
import django_redis
import environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(debug=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


INSTALLED_APPS = [
    'django.contrib.admin',
    # 'n1.apps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.humanize',
    'django.contrib.sites',
    'silk',
    'n1.apps.N1Config',
    'n2.apps.N2Config',
]


MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware', #onlywith DB cache
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'n1.middleware.middleware',
    'final.middleware.RateLimitMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', #onlywith DB cache
]

# APPEND_SLASH = True

ROOT_URLCONF = 'final.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'n1.context_manager.universal_value'
            ],
        },
    },
]

WSGI_APPLICATION = 'final.wsgi.application'
ASGI_APPLICATION = 'final.asgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_FILE_PATH = BASE_DIR / 'sessions'
SESSION_COOKIE_AGE = 60*60*24*7
SESSION_SAVE_EVERY_REQUEST = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,

#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },

#     "root": {
#         "handlers": ["console"],
#         "level": "DEBUG",
#     },
# }
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,

#     "handlers": {
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": "logs/error.log",
#         },
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#         },
#     },

#     "loggers": {
#         "django": {
#             "handlers": ["file", "console"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # DB 1 in Redis
        "TIMEOUT": 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "Decode_Responses": True,
        }
    }
}
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://mymaster/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.SentinelClient",
#             "SENTINELS": [
#                 ("127.0.0.1", 26379),
#             ],
#         },
#        #for multiple sentinels only
#        # "OPTIONS": {
#        #     "CLIENT_CLASS": "django_redis.client.SentinelClient",
#        #     "SENTINELS": [
#        #         ("127.0.0.1", 26379),
#        #         ("127.0.0.1", 26380),
#        #         ("127.0.0.1", 26381),
#        #     ],
#        #     "CONNECTION_POOL_CLASS": "redis.sentinel.SentinelConnectionPool",
#        # },
#     }
# }
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': BASE_DIR / 'cache',
#         'TIMEOUT': 60*2,
#         'OPTIONS': {
#             'MAX_ENTRIES': 1000
#         }
#     }
# }
# CACHES = {#using database for caching
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'cache',
#         'TIMEOUT': 60*2,
#         'OPTIONS': {
#             'MAX_ENTRIES': 1000
#         }
#     }
# }
# python manage.py createcachetable


###production_code
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",

#         # Sentinel nodes (NOT Redis master port)
#         "LOCATION": [
#             "redis://127.0.0.1:26379/1",
#             "redis://127.0.0.1:26380/1",
#             "redis://127.0.0.1:26381/1",
#         ],

#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.SentinelClient",

#             # must match your sentinel.conf
#             "SENTINEL_KWARGS": {
#                 "service_name": "mymaster",
#             },

#             # optional but recommended
#             "CONNECTION_POOL_KWARGS": {
#                 "max_connections": 50,
#             },
#         }
#     }
# }
