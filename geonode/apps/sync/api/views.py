from dynamic_rest.viewsets import DynamicModelViewSet
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter
from geonode.base.api.filters import DynamicSearchFilter
from geonode.base.api.pagination import GeoNodeApiPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import DjangoModelPermissions
from ..models import SynchronizedResource


class SynchronizedResourceViewSet(DynamicModelViewSet):
    http_method_names = ['get']
    authentication_classes = [SessionAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [DjangoModelPermissions]
    filter_backends = [
        DynamicFilterBackend,
        DynamicSortingFilter,
        DynamicSearchFilter,
    ]
    queryset = SynchronizedResource.objects.all().order_by('-created')
    serializer_class = DatasetSerializer
    pagination_class = GeoNodeApiPagination
