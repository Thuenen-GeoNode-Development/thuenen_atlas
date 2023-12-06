from geonode.api.urls import router
from . import views

router.register('sync', views.SyncViewSet, 'sync')

urlpatterns = []