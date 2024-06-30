# Import dj-database-url at the beginning of the file.
import dj_database_url
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-iecure-f2dqc0b$z(7tw-ziq%z2nqx&3l8+d$rd2ko(%fgg_i=jt411-8"
CLIENT_ID = "581342708913-qpjqffdmifi1m24pp6e1vjnmi9g5j6b8.apps.googleusercontent.com"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

RECAPTCHA_SECRET = "6LfNF9kpAAAAAJ78kWfUwbz1nVngDotbmF8Mmmgr"
POLYGON_SECRET = "TKv3e1RjCWUmnaGYvcvg5qEnnprQlXWu"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "martor",
    "sbook",
    "note",
    "chatty",
    "classroom",
    "school",
    "quizz",
    "mdeditor",
]

GOOGLE_ANALYTICS = {
    "google_analytics_id": "G-RLSSV98G86",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sbook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sbook.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
STATIC_URL = "http://localhost/static/"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "sbook.up.railway.app",
    ".railway.app",
    ".up.railway.app",
    "sbook.vercel.app",
    "sbook-j0my.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://sbook.up.railway.app",
    "https://sbook.onrender.com",
    "https://sbook.vercel.app",
    "https://sbook-j0my.onrender.com",
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "engonken8@gmail.com"
EMAIL_HOST_PASSWORD = "amemimy114865009"

DEFAULT_FROM_EMAIL = "noreply<engonken8@gmail.com>"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Douala"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# TEMPLATES = (Path(__file__).resolve().parent / "templates").glob("*.django")
# print(TEMPLATES)

THEMES = {
    "note": "#274",
}


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

MDEDITOR_CONFIGS = {
    "default": {
        "width": "90% ",  # Custom edit box width
        "height": 500,  # Custom edit box height
        "toolbar": [
            "undo",
            "redo",
            "|",
            "bold",
            "del",
            "italic",
            "quote",
            "ucwords",
            "uppercase",
            "lowercase",
            "|",
            "h1",
            "h2",
            "h3",
            "h5",
            "h6",
            "|",
            "list-ul",
            "list-ol",
            "hr",
            "|",
            "link",
            "reference-link",
            "image",
            "code",
            "preformatted-text",
            "code-block",
            "table",
            "datetime",
            "emoji",
            "html-entities",
            "pagebreak",
            "goto-line",
            "|",
            "help",
            "info",
            "||",
            "preview",
            "watch",
            "fullscreen",
        ],  # custom edit box toolbar
        "upload_image_formats": [
            "jpg",
            "jpeg",
            "gif",
            "png",
        ],  # image upload format type
        "image_folder": "editor",  # image save the folder name
        "theme": "dark",  # edit box theme, dark / default
        "preview_theme": "dark",  # Preview area theme, dark / default
        "editor_theme": "dark",  # edit area theme, pastel-on-dark / default
        "toolbar_autofixed": True,  # Whether the toolbar capitals
        "search_replace": True,  # Whether to open the search for replacement
        "emoji": True,  # whether to open the expression function
        "tex": True,  # whether to open the tex chart function
        "flow_chart": True,  # whether to open the flow chart function
        "sequence": True,  # Whether to open the sequence diagram function
        "watch": True,  # Live preview
        "lineWrapping": False,  # lineWrapping
        "lineNumbers": True,  # lineNumbers
        "language": "en",  # zh / en / es
    }
}
