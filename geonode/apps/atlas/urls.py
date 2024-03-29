from django.conf.urls import url

from .views import AtlasDetail, AtlasList

urlpatterns = [
    url(r"^(?P<slug>[-\w]+)$", AtlasDetail.as_view(), name="atlas_detail"),
    url(r"", AtlasList.as_view(), name="atlas_list"),
]
