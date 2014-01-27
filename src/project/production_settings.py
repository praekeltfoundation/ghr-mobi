'''
Created on 23 Jan 2014

@author: sanet
'''
DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ghr',                               # Or path to database file if using sqlite3.
        'USER': 'ghr',                               # Not used with sqlite3.
        'PASSWORD': 'ghr',                                  # Not used with sqlite3.
        'HOST': 'localhost',                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    }
}