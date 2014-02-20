from unipath import FSPath as Path
from django.utils import timezone

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def abspath(*args):
    """convert relative paths to absolute paths relative to PROJECT_ROOT"""
    return os.path.join(PROJECT_ROOT, *args)


APP_NAME = 'Girl Hub Rwanda'

PROJECT_NAME = 'app'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('', ''),
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
MEDIA_ROOT = abspath('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = abspath('static')

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
    'compressor.finders.CompressorFinder',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
    'django.contrib.comments',
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
    'compressor',
    'app',
    'app.authentication',
    'app.articles',
    'app.discussions',
    'app.galleries',
    'app.directory',
    'app.contacts',
    'app.faq',
    'app.newsfeed',
    'app.research_tool',
    'app.root',
    'tunobase',
    'tunobase.core',
    'tunobase.tagging',
    'tunobase.commenting',
    'tunobase.poll',
    'tunobase.social_media',
    'tunobase.social_media.tunosocial',
    'tunobase.social_media.facebook',
    'tunobase.social_media.twitter',
    'tunobase.social_media.google_plus',
    'tunobase.api.vumi',
    'ckeditor',
    'photologue',
    'haystack',
    #'registration',
    'preferences',
    'gunicorn',
    'honeypot',
    'django.contrib.admin'
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

# Poll Settings

ALLOW_CERTAIN_POLL_MULTIPLE_ANSWERS = True
ANONYMOUS_POLL_VOTES_ALLOWED = True

# Whoosh Settings

WHOOSH_PATH = abspath('whoosh')

# Haystack Settings

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_PATH.child('whoosh_index'),
    },
}

# Commenting Settings

COMMENT_FLAGS_FOR_REMOVAL = 3
ANONYMOUS_COMMENTS_ALLOWED = True
COMMENT_PERIOD_LOCKOUT = timezone.timedelta(minutes=1)
NUM_COMMENTS_ALLOWED_IN_PERIOD = 5

# Liking Settings

ANONYMOUS_LIKES_ALLOWED = True
LIKE_PERIOD_LOCKOUT = timezone.timedelta(minutes=1)
NUM_LIKES_ALLOWED_IN_PERIOD = 5

# Registration Settings

REGISTRATION_ACTIVATION_REQUIRED = False
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/authentication/secure/login/'
AUTH_USER_MODEL = 'authentication.EndUser'
SESSION_COOKIE_AGE = 24 * 60 * 60
INTERNAL_IPS = ('127.0.0.1',)

# Django Celery Settings
CELERY_ALWAYS_EAGER = False
BROKER_URL = 'amqp://ghr:ghr@127.0.0.1:5672//ghr'

# Honeypot Settings

HONEYPOT_FIELD_NAME = 'ghr_hp'
HONEYPOT_VALUE = 'ghr'


# CK Editor Settings

CKEDITOR_UPLOAD_PATH = MEDIA_ROOT.child('uploads')
CKEDITOR_STATIC_PREFIX = '/static/ckeditor/'

# Default Image Settings

DEFAULT_IMAGE_CATEGORY_CHOICES = (
    ('content', 'Content'),
    ('user', 'User'),
)

# Vumi API Settings

VUMI_ACCOUNT_KEY = ''
VUMI_CONVERSATION_KEY = ''
VUMI_URL = 'https://go.vumi.org/api/v1/go/http_api/%s/messages.json' % VUMI_CONVERSATION_KEY
VUMI_ACCESS_TOKEN = ''

# Authentication Backend Settings

AUTHENTICATION_BACKENDS = (
    'app.authentication.backends.MobileUsernameBackend',
)


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
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'mail': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
        },
    }
}

try:
    from production_settings import *
except ImportError:
    pass
