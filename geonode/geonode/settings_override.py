# -*- coding: utf-8 -*-
import os
import ast
import logging
from urllib.parse import urljoin

# load the defaults settings
from geonode.settings import *  # noqa
from geonode.settings import (  # noqa
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


# relax origins for geonode-mapstore-client development
CSRF_TRUSTED_ORIGINS = (
    ["http://172.18.0.1:8001", "http://localhost:8081"]
    if DEBUG
    else ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]"))
)  # noqa
CORS_ALLOWED_ORIGINS = (
    ["http://172.18.0.1:8001", "http://localhost:8081"]
    if DEBUG
    else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))
)  # noqa


STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"


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
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
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
    "subsites",
    "externalapplications",
    "importer_datapackage",
    "thuenen_app",
)

ENABLE_SUBSITE_CUSTOM_THEMES = True

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

LDAP_ENABLED = ast.literal_eval(os.getenv("LDAP_ENABLED", "False"))

if LDAP_ENABLED:
    from django_auth_ldap import config as ldap_config
    # from geonode_ldap.config import GeonodeNestedGroupOfNamesType
    import ldap

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

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en")
GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = os.getenv("GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY", "mapstore")
SITE_HOST_SCHEMA = os.getenv("SITE_HOST_SCHEMA", "http")
SITE_HOST_NAME = os.getenv("SITE_HOST_NAME", "localhost")
SITE_HOST_PORT = os.getenv("SITE_HOST_PORT", 8000)
_default_siteurl = (
    f"{SITE_HOST_SCHEMA}://{SITE_HOST_NAME}:{SITE_HOST_PORT}/"
    if SITE_HOST_PORT
    else f"{SITE_HOST_SCHEMA}://{SITE_HOST_NAME}/"
)
DEFAULT_TILE_SIZE = os.environ.get("DEFAULT_TILE_SIZE", 512)
SITEURL = os.getenv("SITEURL", _default_siteurl)

# CSW settings
CATALOGUE = {
    "default": {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        "ENGINE": os.getenv("CATALOGUE_ENGINE", "geonode.catalogue.backends.pycsw_local"),
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',
        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        "URL": os.getenv("CATALOGUE_URL", urljoin(SITEURL, "/catalogue/csw")),
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',
        # 'ALTERNATES_ONLY': True,
    }
}

# pycsw settings
PYCSW = {
    # pycsw configuration
    "CONFIGURATION": {
        # uncomment / adjust to override server config system defaults
        # 'server': {
        #    'maxrecords': '10',
        #    'pretty_print': 'true',
        #    'federatedcatalogues': 'http://catalog.data.gov/csw'
        # },
        "server": {
            "home": ".",
            "url": CATALOGUE["default"]["URL"],
            "encoding": "UTF-8",
            "language": LANGUAGE_CODE if LANGUAGE_CODE in ("en", "fr", "el") else "en",
            "maxrecords": "20",
            "pretty_print": "true",
            # 'domainquerytype': 'range',
            "domaincounts": "true",
            "profiles": "apiso,ebrim",
        },
        "manager": {
            # authentication/authorization is handled by Django
            "transactions": "false",
            "allowed_ips": "*",
            # 'csw_harvest_pagesize': '10',
        },
        "metadata": {
            "inspire": {
                "enabled": True,
                "languages_supported": "eng,gre",
                "default_language": "eng",
                "date": "YYYY-MM-DD",
                "gemet_keywords": "Utility and governmental services",
                "conformity_service": "notEvaluated",
                "contact_name": "Organization Name",
                "contact_email": "Email Address",
                "temp_extent": {
                    "begin": "YYYY-MM-DD",
                    "end": "YYYY-MM-DD",
                },
            },
            "identification": {
                "title": "GeoNode Catalogue",
                "description": "GeoNode is an open source platform"
                " that facilitates the creation, sharing, and collaborative use"
                " of geospatial data",
                "keywords": "sdi, catalogue, discovery, metadata," " GeoNode",
                "keywords_type": "theme",
                "fees": "None",
                "accessconstraints": "None",
            },
            "provider": {
                "name": "Organization Name",
                "url": SITEURL,
            },
            "contact": {
                "name": "Lastname, Firstname",
                "position": "Position Title",
                "address": "Mailing Address",
                "city": "City",
                "stateorprovince": "Administrative Area",
                "postalcode": "Zip or Postal Code",
                "country": "Country",
                "phone": "+xx-xxx-xxx-xxxx",
                "fax": "+xx-xxx-xxx-xxxx",
                "email": "Email Address",
                "url": "Contact URL",
                "hours": "Hours of Service",
                "instructions": "During hours of service. Off on " "weekends.",
                "role": "pointOfContact",
            },
        },
    }
}

"""
MapStore2 REACT based Client parameters
"""
if GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY == "mapstore":
    GEONODE_CLIENT_HOOKSET = os.getenv("GEONODE_CLIENT_HOOKSET", "geonode_mapstore_client.hooksets.MapStoreHookSet")

    if "geonode_mapstore_client" not in INSTALLED_APPS:
        INSTALLED_APPS += ("geonode_mapstore_client",)

    def get_geonode_catalogue_service():
        if PYCSW:
            pycsw_config = PYCSW["CONFIGURATION"]
            if pycsw_config:
                pycsw_catalogue = {
                    f"{pycsw_config['metadata']['identification']["title"]}": {
                        "url": CATALOGUE["default"]["URL"],
                        "type": "csw",
                        "title": pycsw_config["metadata"]["identification"]["title"],
                        "autoload": True,
                        "layerOptions": {"tileSize": DEFAULT_TILE_SIZE},
                    }
                }
                return pycsw_catalogue
        return None

    GEONODE_CATALOGUE_SERVICE = get_geonode_catalogue_service()
