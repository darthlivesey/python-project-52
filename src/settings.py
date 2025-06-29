import os
import rollbar
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from django.utils.translation import gettext as _

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

TESTING = 'test' in sys.argv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'hexlet-code-d230.onrender.com',
    'localhost',
    '127.0.0.1',
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'whitenoise.runserver_nostatic',
    'django_bootstrap5',
    'task_manager',
    'tests',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

for path in LOCALE_PATHS:
    ru_mo_path = path / 'ru/LC_MESSAGES/django.mo'
    print(f"Checking translation: {ru_mo_path} - exists: {ru_mo_path.exists()}")

USE_I18N = True

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'task_manager' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'task_manager.context_processors.language_context', 
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
            conn_max_age=600,
            engine='django.db.backends.postgresql'
        )
    }

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

LANGUAGE_CODE = 'ru' if not TESTING else 'en'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP5 = {
    'theme_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

if not TESTING:
    ROLLBAR = {
        'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
        'environment': os.getenv('ROLLBAR_ENVIRONMENT', 'development'),
        'code_version': '1.0',
        'root': BASE_DIR,
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'rollbar': {
                'class': 'rollbar.logger.RollbarHandler',
                'access_token': ROLLBAR['access_token'],
                'environment': ROLLBAR['environment'],
            },
        },
        'loggers': {
            'django': {
                'handlers': ['rollbar'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
else:
    LOGGING = {}
    LANGUAGE_CODE = 'en'

if not TESTING and not DEBUG and os.getenv('ROLLBAR_ACCESS_TOKEN'):
    import rollbar
    rollbar.init(
        os.getenv('ROLLBAR_ACCESS_TOKEN'),
        environment=os.getenv('ROLLBAR_ENVIRONMENT', 'production'),
        root=BASE_DIR,
    )
    
    MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404')
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'rollbar': {
                'class': 'rollbar.logger.RollbarHandler',
                'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
                'environment': os.getenv('ROLLBAR_ENVIRONMENT', 'production'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['rollbar'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    LOGGING = {}

WHITENOISE_MAX_AGE = 0
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print("\n" + "="*50)
print(f"BASE_DIR: {BASE_DIR}")
print(f"LOCALE_PATHS: {LOCALE_PATHS}")

for path in LOCALE_PATHS:
    full_path = path
    print(f"\nChecking: {full_path}")
    print(f"Exists: {full_path.exists()}")
    
    if full_path.exists():
        ru_path = full_path / 'ru/LC_MESSAGES/django.mo'
        print(f"Russian translation exists: {ru_path.exists()}")
    
print("="*50 + "\n")
