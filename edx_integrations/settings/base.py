import os
import platform
from logging.handlers import SysLogHandler
from os.path import abspath, dirname, join
from sys import path

here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

path.append(root('apps'))

SECRET_KEY = os.environ.get('EDX_INTEGRATIONS_SECRET_KEY', 'insecure-secret-key')

# Application definition
INSTALLED_APPS = [
]

THIRD_PARTY_APPS = [
]

PROJECT_APPS = [
    'edx_integrations.salesforce',
]


INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Set this value in the environment-specific files (e.g. local.py, production.py, test.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edxapp',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    },
    'ecomm': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    root('conf', 'locale'),
)


# Use a different address for Mac OS X
syslog_address = '/var/run/syslog' if platform.system().lower() == 'darwin' else '/dev/log'
syslog_format = '[service_variant=discovery][%(name)s] %(levelname)s [{hostname}  %(process)d] ' \
                '[%(pathname)s:%(lineno)d] - %(message)s'.format(hostname="salesforce")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d [%(name)s] %(pathname)s:%(lineno)d - %(message)s',
        },
        'syslog_format': {'format': syslog_format},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'local': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'address': syslog_address,
            'formatter': 'syslog_format',
            'facility': SysLogHandler.LOG_LOCAL0,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'local'],
            'propagate': True,
            'level': 'INFO'
        },
    }
}


