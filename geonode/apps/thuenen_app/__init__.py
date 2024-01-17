import os
from django.apps import AppConfig


def run_setup_hooks(*args, **kwargs):
    from django.conf import settings
    from django.conf.urls import url
    from django.views.generic import TemplateView
    from geonode.urls import urlpatterns

    LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(LOCAL_ROOT, "templates")
    settings.TEMPLATES[0]["DIRS"].insert(0, template_dir)
    
    urlpatterns += [
        url(r'^legal_notice/$',
            TemplateView.as_view(template_name='legal-notice.html'),
            name='legal-notice'),
        url(r'^accessibility/$',
            TemplateView.as_view(template_name='accessibility.html'),
            name='accessibility'),
    ]


class ThuenenAppConfig(AppConfig):
    name = 'thuenen_app'

    def ready(self):
        super().ready()
        run_setup_hooks()

default_app_config = 'thuenen_app.ThuenenAppConfig'
