from pathlib import Path
import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

DEBUG = os.environ.get('DEBUG', 'True').lower() in {'true', '1', 'yes'}

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY must be configured when DEBUG is disabled.'
        )
    SECRET_KEY = 'django-insecure-development-only-key'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1',
    ).split(',')
    if host.strip()
]
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f'https://{render_hostname}')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django built-in apps
    'daphne',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'channels',

    # Local apps
    'seashell_parallel',
]

AUTH_USER_MODEL = 'seashell_parallel.User'


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL / APPLICATION CONFIGURATION
# ============================================================

ROOT_URLCONF = 'mainProject.urls'

# Change this one path to replace the logo throughout the application.
SEASTEM_LOGO = 'images/logo.png'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Global template directory
        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainProject.context_processors.branding',
            ],
        },
    },
]


# ============================================================
# ASGI
# ============================================================

ASGI_APPLICATION = 'mainProject.asgi.application'


# ============================================================
# DATABASE
# ============================================================
database_url = os.environ.get('DATABASE_URL')
if not DEBUG and not database_url:
    raise ImproperlyConfigured(
        'DATABASE_URL must be configured when DEBUG is disabled.'
    )

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR.as_posix()}/db.sqlite3',
        conn_max_age=600,
    ),
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': (
            'storages.backends.s3.S3Storage'
            if os.environ.get('AWS_STORAGE_BUCKET_NAME')
            else 'django.core.files.storage.FileSystemStorage'
        ),
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}


# ============================================================
# MEDIA FILES
# ============================================================
# Uploaded seaweed images will be stored here during development.

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL') or None
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False
ALLOW_EPHEMERAL_MEDIA = (
    os.environ.get('ALLOW_EPHEMERAL_MEDIA', 'False').lower()
    in {'true', '1', 'yes'}
)

if not DEBUG:
    if AWS_STORAGE_BUCKET_NAME and not all((
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_S3_REGION_NAME,
    )):
        raise ImproperlyConfigured(
            'S3 media storage requires AWS_ACCESS_KEY_ID, '
            'AWS_SECRET_ACCESS_KEY, and AWS_S3_REGION_NAME.'
        )
    if not AWS_STORAGE_BUCKET_NAME and not ALLOW_EPHEMERAL_MEDIA:
        raise ImproperlyConfigured(
            'Configure S3 media storage or explicitly enable '
            'ALLOW_EPHEMERAL_MEDIA for a disposable deployment.'
        )


# ============================================================
# DJANGO CHANNELS
# ============================================================

REDIS_URL = os.environ.get('REDIS_URL')
if not DEBUG and not REDIS_URL:
    raise ImproperlyConfigured(
        'REDIS_URL must be configured when DEBUG is disabled.'
    )
REDIS_URL = REDIS_URL or 'redis://127.0.0.1:6379/0'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [REDIS_URL]},
    },
}


# ============================================================
# CELERY
# ============================================================

CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = (
    os.environ.get('CELERY_TASK_ALWAYS_EAGER', 'False').lower()
    in {'true', '1', 'yes'}
)
CELERY_TASK_EAGER_PROPAGATES = True

CELERY_ACCEPT_CONTENT = [
    'json',
]

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Asia/Manila'

CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_TASK_ACKS_LATE = True

CELERY_TASK_TRACK_STARTED = True


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

LOGIN_URL = 'signin'


# ============================================================
# EMAIL
# ============================================================
# Development only: emails appear in the terminal.

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
)


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


