# -*- coding: utf-8 -*-
import os

# load the defaults settings
from geonode.settings import *
from geonode.settings import TEMPLATES, INSTALLED_APPS, IMPORTER_HANDLERS


SITENAME = os.getenv("SITENAME", "thuenen_atlas")
X_FRAME_OPTIONS = "SAMEORIGIN"


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

# Additional directories which hold static files
# - Give priority to local ones
TEMPLATES[0]["DIRS"].insert(0, "/usr/src/geonode/templates")
loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
TEMPLATES[0]["OPTIONS"]["loaders"] = loaders
TEMPLATES[0].pop("APP_DIRS", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d "
            "%(thread)d %(message)s"
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "geonode": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "owslib": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "pycsw": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "celery": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "geonode_logstash.logstash": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

IMPORTER_HANDLERS = (
    "importer_datapackage.handlers.datapackage.handler.DataPackageFileHandler",
    *IMPORTER_HANDLERS,
)

INSTALLED_APPS += (
    "atlas",
    "externalapplications",
    "importer_datapackage",
    "thuenen_app",
)

# LDAP
# WE DO NOT USE CONTRIB APP BUT
# django-auth-ldap
# Add your specific LDAP configuration after this comment:
# https://pypi.org/project/django-auth-ldap/
# --------------------------------------------------
# LDAP conf:

from django_auth_ldap import config as ldap_config

# from geonode_ldap.config import GeonodeNestedGroupOfNamesType
import ldap

LDAP_ENABLED = ast.literal_eval(os.getenv("LDAP_ENABLED", "False"))

# enable logging
import logging

logger = logging.getLogger("django_auth_ldap")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# add both standard ModelBackend auth and django_auth_ldap.backend.LDAPBackend auth
AUTHENTICATION_BACKENDS += ("django_auth_ldap.backend.LDAPBackend",)

# django_auth_ldap configuration
AUTH_LDAP_SERVER_URI = os.getenv("LDAP_SERVER_URL")
AUTH_LDAP_BIND_DN = os.getenv("LDAP_BIND_DN")
AUTH_LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD")

# USER
AUTH_LDAP_USER_SEARCH = ldap_config.LDAPSearch(
    os.getenv("LDAP_USER_SEARCH_DN"),
    ldap.SCOPE_SUBTREE,
    os.getenv("LDAP_USER_SEARCH_FILTERSTR"),
)
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# GROUPS
# Group mirroring is not working since GeoNode does not
# use the standard Django group models. Since geonode-ldap contrib
# app is very old and badly maintained we will use django-auth-ldap
# instead. For this we need to disable groups:
AUTH_LDAP_MIRROR_GROUPS = False
AUTH_LDAP_FIND_GROUP_PERMS = False
AUTH_LDAP_MIRROR_GROUPS_EXCEPT = False
# AUTH_LDAP_GROUP_SEARCH = ldap_config.LDAPSearch(
#     os.getenv("LDAP_GROUP_SEARCH_DN"),
#     ldap.SCOPE_SUBTREE,
#     os.getenv("LDAP_GROUP_SEARCH_FILTERSTR")
# )
# # see comment above
# # AUTH_LDAP_GROUP_TYPE = GeonodeNestedGroupOfNamesType()

# # these are not needed by django_auth_ldap - we use them to find and match
# # GroupProfiles and GroupCategories
# GEONODE_LDAP_GROUP_NAME_ATTRIBUTE = os.getenv("LDAP_GROUP_NAME_ATTRIBUTE", default="cn")
# GEONODE_LDAP_GROUP_PROFILE_FILTERSTR = os.getenv("LDAP_GROUP_SEARCH_FILTERSTR", default='(ou=research group)')
# GEONODE_LDAP_GROUP_PROFILE_MEMBER_ATTR = os.getenv("LDAP_GROUP_PROFILE_MEMBER_ATTR", default='member')
# --------------------------------------------------
