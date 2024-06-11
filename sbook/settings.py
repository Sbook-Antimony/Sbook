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
    "quizz",
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
STATIC_URL = "http://sbook.up.railway.app/static/"

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


# Choices are: "semantic", "bootstrap"
MARTOR_THEME = 'bootstrap'

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'true',        # to enable/disable imgur/custom uploader.
    'mention': 'false',     # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery
    'living': 'false',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]

# To setup the martor editor with title label or not (default is False)
MARTOR_ENABLE_LABEL = False

# Disable admin style when using custom admin interface e.g django-grappelli
MARTOR_ENABLE_ADMIN_CSS = True

# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = '1342e05a9f40019'
MARTOR_IMGUR_API_KEY = '448dda190d0b4739333353f721ff9b218460a232'

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'  # default
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/'  # default

MARTOR_MARKDOWNIFY_TIMEOUT = 0

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',
    'markdown.extensions.sane_lists',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',      # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',      # to parse markdown mention
    'martor.extensions.emoji',        # to parse markdown emoji
    'martor.extensions.mdx_video',    # to parse embed/iframe video
    'martor.extensions.escape_html',  # to handle the XSS vulnerabilities
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

MARTOR_UPLOAD_URL = '/martor/uploader/'  # default

MARTOR_SEARCH_USERS_URL = '/martor/search-user/'  # default

# Markdown Extensions
MARTOR_MARKDOWN_BASE_EMOJI_URL = (
    'https://github.githubassets.com'
    '/images/icons/emoji/'
)
MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://sbook.up.railway.app/author/'
# please change this to your domain

# If you need to use your own themed "bootstrap" or "semantic ui" dependency
# replace the values with the file in your static files dir
MARTOR_ALTERNATIVE_JS_FILE_THEME = "semantic-themed/semantic.min.js"
MARTOR_ALTERNATIVE_CSS_FILE_THEME = "semantic-themed/semantic.min.css"
MARTOR_ALTERNATIVE_JQUERY_JS_FILE = "jquery/dist/jquery.min.js"

# URL schemes that are allowed within links
ALLOWED_URL_SCHEMES = [
    "file", "ftp", "ftps", "http", "https", "irc", "mailto",
    "sftp", "ssh", "tel", "telnet", "tftp", "vnc", "xmpp",
]

# https://gist.github.com/mrmrs/7650266
ALLOWED_HTML_TAGS = [
    "a", "abbr", "b", "blockquote", "br", "cite", "code", "command",
    "dd", "del", "dl", "dt", "em", "fieldset", "h1", "h2", "h3", "h4", "h5",
    "h6", "hr", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend",
    "li", "ol", "optgroup", "option", "p", "pre", "small", "span", "strong",
    "sub", "sup", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "u",
    "ul"
]

# https://github.com/decal/werdlists/blob/master/html-words/html-attributes-list.txt
ALLOWED_HTML_ATTRIBUTES = [
    "alt", "class", "color", "colspan", "datetime",  # "data",
    "height", "href", "id", "name", "reversed", "rowspan",
    "scope", "src", "style", "title", "type", "width"
]

CSRF_COOKIE_HTTPONLY = False
