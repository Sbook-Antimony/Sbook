# Import dj-database-url at the beginning of the file.
import dj_database_url, os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f2dqc0b$z(7tw-ziq%z2nqx&3l8+d$rd2ko(%fgg_i=jt411-8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

RECAPTCHA_SECRET = "6LfNF9kpAAAAAJ78kWfUwbz1nVngDotbmF8Mmmgr"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'google_analytics',
    'fontawesomefree',
    'sbook',
    'note',
    'chatty',
    'classroom',
]

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'G-RLSSV98G86',
}

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

ROOT_URLCONF = 'sbook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sbook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if os.getenv('ENV') == 'render':
    DATABASES = {
        'default': dj_database_url.config(
            # Replace this value with your local database's connection string.
            default='postgresql://postgres:dpg-co0tm3mn7f5s73dt8hlg-a@sbook.onrender.com:5432/sbook',
            conn_max_age=600
        )
    }
    STATIC_URL = '/static/'

    ALLOWED_HOSTS = ["sbook.onrender.com"]
elif os.getenv('ENV') == 'vercel':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    STATIC_URL = '/static/'
    ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]
elif os.getenv('ENV') == 'railway':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    STATIC_URL = '/static/'
    ALLOWED_HOSTS = ["127.0.0.1", "sbook.up.railway.app"]
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    STATIC_URL = '/static/'

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "sbook.up.railway.app",
    "sbook.vercel.app",
    "sbook.onrender.com",
]

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "engonken8@gmail.com"
EMAIL_HOST_PASSWORD = 'amemimy114865009'

DEFAULT_FROM_EMAIL = 'noreply<engonken8@gmail.com>'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Douala'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# This production code might break development mode, so we check whether we're in DEBUG mode

# Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)

# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching

#All set! We’re ready 

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# TEMPLATES = (Path(__file__).resolve().parent / "templates").glob("*.django")
# print(TEMPLATES)
