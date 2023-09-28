# -*- coding: utf-8 -*-
import os
# load the defaults settings
from geonode.settings import *
from geonode.settings import TEMPLATES, INSTALLED_APPS, IMPORTER_HANDLERS


SITENAME = os.getenv("SITENAME", 'thuenen_atlas')


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

# Additional directories which hold static files
# - Give priority to local ones
TEMPLATES[0]['DIRS'].insert(0, "/usr/src/geonode/templates")
loaders = ['django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader']
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode": {
            "handlers": ["console"], "level": "DEBUG", },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"], "level": "DEBUG", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        "celery": {
            "handlers": ["console"], "level": "DEBUG", },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode_logstash.logstash": {
            "handlers": ["console"], "level": "DEBUG", },
    },
}

IMPORTER_HANDLERS = (
    'importer_datapackage.handlers.datapackage.handler.DataPackageFileHandler',
    *IMPORTER_HANDLERS,
)

INSTALLED_APPS += ("atlas",
                   "externalapplications",
                   "importer_datapackage",
                   "thuenen_app")
