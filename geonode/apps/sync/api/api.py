from geonode.api.urls import router
from . import views

router.register("sync", views.SynchronizedResourceViewSet, "sync")

urlpatterns = []
