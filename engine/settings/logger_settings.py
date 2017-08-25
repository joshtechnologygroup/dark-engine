# Logger Configurations
from pythonjsonlogger import jsonlogger
from os.path import dirname, abspath, join, exists
import os
import sys


class LoggerSettingsMixin(object):

    # Create a local log directory if log_file does not exist.
    root = dirname(dirname(dirname(abspath(__file__))))
    log_dir = join(root, 'log')
    if not exists(log_dir):
        os.makedirs(log_dir)
    file_name = join(log_dir, 'apis.log')

    LOG_FILE = os.environ.get('LOG_FILE', file_name)

    if os.getenv('MANAGEMENT_SCRIPT', False):
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'simple': {
                    'format': '%(levelname)s %(message)s'
                }
            },
            'handlers': {
                 'stdout': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'stream': sys.stdout
                 }
            },
            'loggers': {
                 '': {
                    'handlers': ['stdout'],
                    'propagate': True,
                    'level': 'INFO',
                 },
            }
        }
    else:
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)s [%(levelname)s] logger=%(name)s '
                              'process=%(process)d thread=%(thread)d %(message)s'
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                },
                'json': {
                    '()': jsonlogger.JsonFormatter,
                    'fmt': '%(asctime)s %(levelname)s %(name)s %(thread)d %(process)d %(message)s'
                }
            },
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse'
                }
            },
            'handlers': {
                'null': {
                    'level': 'DEBUG',
                    'class': 'logging.NullHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                },
                'mail_admins': {
                    'level': 'ERROR',
                    'filters': ['require_debug_false'],
                    'class': 'django.utils.log.AdminEmailHandler',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['console'],
                    'propagate': True,
                    'level': 'INFO',
                },
                'django.request': {
                    'handlers': ['mail_admins'],
                    'level': 'ERROR',
                    'propagate': False,
                },
                'django.db.backends': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'apps': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': False,
                },

                # Catch All Logger -- Captures any other logging
                '': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': True,
                }
            }
        }
