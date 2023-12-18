from . import views
from geonode.api.urls import router

router.register(r"sync", views.ReceivePushedDataViewSet)

urlpatterns += router.urls
