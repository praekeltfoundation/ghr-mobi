import datetime

from unipath import FSPath as Path

BUILDOUT_PATH = Path(__file__).parent.parent.parent

APP_NAME = 'Unomena Starter'

PROJECT_NAME = 'unomena'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Unomena Developers', 'dev@unomena.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s.sqlite' % PROJECT_NAME,     # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BUILDOUT_PATH.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = BUILDOUT_PATH.child('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z^uq$7x5jn%1nove38w+crkd9k8pq4=p8v*$h%h93-)b88uu@7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'project.context_processors.project_settings',
    'preferences.context_processors.preferences_cp',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    #BUILDOUT_PATH.child('eggs').child('django_debug_toolbar-0.9.4-py2.7.egg').child('debug_toolbar').child('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    #'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django_countries',
    'polymorphic',
    'debug_toolbar',
    'djcelery',
    'south',
    'tunobase',
    'tunobase.core',
    'tunobase.console',
    'tunobase.mailer',
    'tunobase.corporate.company_info',
    'tunobase.corporate.media',
    'tunobase.blog',
    'tunobase.age_gate',
    'tunobase.bulk_loading',
    'tunobase.commenting',
    'tunobase.tagging',
    'unomena',
    'unomena.auth',
    'unomena.core',
    'ckeditor',
    'photologue',
    #'registration',
    'preferences',
    'gunicorn',
    'honeypot',
    'django.contrib.admin',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 15
    }
}

# Debug Toolbar Settings

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

# Age Gate Settings

AGE_GATE_LOCATION_CHOICES = (('za', 'South Africa'),)
AGE_GATE_MIN_NUM_YEARS_BACK = 73
AGE_GATE_MAX_NUM_YEARS_BACK = 0

AGE_GATE_COUNTRY_LEGAL_AGES = {
    'za': 18
}

# Registration Settings

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/secure/login/'
AUTH_USER_MODEL = 'auth.EndUser'
SESSION_COOKIE_AGE = 24 * 60 * 60

INTERNAL_IPS = ('127.0.0.1',)


# Django Celery Settings

BROKER_URL = 'amqp://unomena:unomena@127.0.0.1:5672//unomena'

# Honeypot Settings

HONEYPOT_FIELD_NAME = 'unomena_hp'
HONEYPOT_VALUE = 'unomena'


# CK Editor Settings

CKEDITOR_UPLOAD_PATH = MEDIA_ROOT.child('uploads')
CKEDITOR_STATIC_PREFIX = '/static/ckeditor/'


# Email Settings

EMAIL_ENABLED = False
DEFAULT_FROM_EMAIL = 'Unomena <unomena.com>'
CONTACT_MESSAGE_TO_EMAIL = 'dev@unomena.com'
EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.unomena.net'
EMAIL_HOST_USER = 'mailman'
EMAIL_HOST_PASSWORD = 'AKmiQldQ2e'

# Default Image Settings

DEFAULT_IMAGE_CATEGORY_CHOICES = (('content', 'Content'),)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(module)s.%(funcName)s:  %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'unomena': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

try:
    from project.settings_local import *
except ImportError:
    pass