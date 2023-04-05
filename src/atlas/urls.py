from django.conf.urls import url

from .views import AtlasDetail, AtlasList, AtlasDetailView

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)$', AtlasDetail.as_view(), name='atlas-detail'),
    url(r'', AtlasList.as_view(), name='atlas-list'),
]

