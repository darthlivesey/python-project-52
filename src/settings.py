import os
import sys
import dj_database_url
from dotenv import load_dotenv
from django.utils.translation import gettext as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f"Absolute path to settings.py: {os.path.abspath(__file__)}")
print(f"Computed BASE_DIR: {BASE_DIR}")

load_dotenv(os.path.join(BASE_DIR, '.env'))

TESTING = 'test' in sys.argv

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
    os.path.join(BASE_DIR, 'locale'),
]

if not TESTING:
    from django.core.management import call_command
    po_path = os.path.join(BASE_DIR, 'locale', 'ru', 'LC_MESSAGES', 'django.po')
    if os.path.exists(po_path):
        try:
            call_command('compilemessages', verbosity=0)
            print("Successfully compiled translations")
        except Exception as e:
            print(f"Error compiling translations: {e}")

USE_I18N = True
ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'task_manager', 'templates')],
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

WSGI_APPLICATION = 'src.wsgi.application'

if DEBUG or TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP5 = {
    'theme_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

ROLLBAR_ACCESS_TOKEN = os.getenv('ROLLBAR_ACCESS_TOKEN')
if ROLLBAR_ACCESS_TOKEN and not DEBUG and not TESTING:
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': os.getenv('ROLLBAR_ENVIRONMENT', 'production'),
        'root': BASE_DIR,
    }
    MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'rollbar': {
                'class': 'rollbar.logger.RollbarHandler',
                'access_token': ROLLBAR_ACCESS_TOKEN,
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
else:
    LOGGING = {}

if TESTING:
    LANGUAGE_CODE = 'en'
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

print("\n" + "="*50)
print(f"LOCALE_PATHS: {LOCALE_PATHS}")

for path in LOCALE_PATHS:
    print(f"\nChecking: {path}")
    print(f"Exists: {os.path.exists(path)}")
    
    if os.path.exists(path):
        po_path = os.path.join(path, 'ru/LC_MESSAGES/django.po')
        mo_path = os.path.join(path, 'ru/LC_MESSAGES/django.mo')
        print(f"Russian PO file exists: {os.path.exists(po_path)}")
        print(f"Russian MO file exists: {os.path.exists(mo_path)}")
    
print("="*50 + "\n")
