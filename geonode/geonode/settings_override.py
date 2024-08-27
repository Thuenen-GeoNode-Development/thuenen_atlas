# -*- coding: utf-8 -*-
import os
import ast
import logging

# load the defaults settings
from geonode.settings import *
from geonode.settings import (
    DEBUG,
    TEMPLATES,
    INSTALLED_APPS,
    IMPORTER_HANDLERS,
    LOCALE_PATHS,
    PROJECT_ROOT,
    AUTHENTICATION_BACKENDS,
)


SITENAME = os.getenv("SITENAME", "thuenen_atlas")
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None if DEBUG else "same-origin"
# required for geonode-mapstore-client development
CSRF_TRUSTED_ORIGINS = [
    "http://172.18.0.1:8001",
    "http://localhost:8081"
] if DEBUG else []
CORS_ALLOWED_ORIGINS = ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))


STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"


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
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {
            "level": "WARNING",
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
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
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
            "level": "INFO",
        },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "geonode_logstash.logstash": {
            "handlers": ["console"],
            "level": "INFO",
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

# add extra translations
# add to .po file in thuenen_atlas/geonode/apps/thuenen_app/locale
LOCALE_PATHS += (
    os.path.join(PROJECT_ROOT, 'thuenen_app', 'locale'),
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
import ast

LDAP_ENABLED = ast.literal_eval(os.getenv("LDAP_ENABLED", "False"))

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
