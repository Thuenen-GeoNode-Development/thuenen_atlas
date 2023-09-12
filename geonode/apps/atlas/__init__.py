import os
from django.apps import AppConfig
from django.conf.urls import url

import logging

logger = logging.getLogger(__name__)


def run_setup_hooks(*args, **kwargs):
    from django.conf import settings
    from geonode.urls import urlpatterns
    from atlas.views import AtlasView, AtlasDetail

    urlpatterns += [
        url(
            r"^atlanten/(?P<slug>[-\w]+)$",
            AtlasDetail.as_view(
                template_name="geonode-mapstore-client/atlas_detail.html"
            ),
        ),
        url(
            r"^atlanten/",
            AtlasView.as_view(
                template_name="geonode-mapstore-client/atlas_list.html"
            ),
        ),
    ]


class ThuenenAtlasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "atlas"
    default_model = "Atlas"

    def ready(self):
        super().ready()
        run_setup_hooks()


default_app_config = "atlas.ThuenenAtlasConfig"
