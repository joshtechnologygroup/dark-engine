from . import base


class Settings(base.Settings):

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dark_engine',                      # Or path to database file if using sqlite3.
            'USER': 'admin',                      # Not used with sqlite3.
            'PASSWORD': 'admin',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': ''                       # Set to empty string for default. Not used with sqlite3.
        }
    }

    DEBUG = True
