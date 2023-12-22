import os
import json
import time
import typing
import inspect
import logging
import requests
import importlib

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.apps import apps

from geonode.base.models import ResourceBase
from geonode.base.api.serializers import ResourceBaseSerializer, BaseDynamicModelSerializer

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import authentication
from rest_framework import permissions
from oauth2_provider.contrib import rest_framework

from ..apps import BASE_FILE, ORIG_RESOURCE, DATA_FILE, STYLE_FILE, THUMBNAIL_FILE
from ..serializers import create_serializer

logger = logging.getLogger(__name__)


class ReceivePushedDataViewSet(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
        rest_framework.OAuth2Authentication,
    ]
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["post"])
    def post(self, request, format=None):
        
        uuid = request.data["uuid"]
        force = request.data["force"]
        resources_exists = ResourceBase.objects.filter(uuid = uuid).exists()
        if resources_exists and force == "False":
            return JsonResponse(status=400, data={
                "error": f"Resource {uuid} exists and force is not true!"
            })
        
        orig_resource = json.load(request.FILES[ORIG_RESOURCE])
        resource_type = orig_resource["resource_type"]
        _resource_type, _serializer = _resolve_type_serializer(resource_type)
        resource_data = _serializer(data=orig_resource)
        
        pushed_resource = json.load(request.FILES[BASE_FILE])
        sync_serializer = create_serializer(resource_data.get_model())
        data = sync_serializer(pushed_resource)
        
        data = {
            "uuid": uuid,
            # TODO check if flag works, otherwise we have to delete resource manually
            "overwrite_existing_layer": force,
        }
        
        # prepare importer "upload"
        data_file = request.FILES[DATA_FILE]
        style_file = request.FILES[STYLE_FILE]
        thumbnail_file = request.FILES[THUMBNAIL_FILE]
        files = {
            "base_file": (data_file.name, data_file, data_file.content_type),
            "thumbnail": (thumbnail_file.name, thumbnail_file, thumbnail_file.content_type),
            "style": (style_file.name, style_file, style_file.content_type)
        }
        
        try:
            auth = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))
            # TODO do it on localhost?
            url = f"{settings.SITEURL}api/v2/uploads/upload"
            # TODO remove webhook.site
            #url = "https://webhook.site/20feca89-00f7-4d8b-943f-df7f20a6c901"
            response = requests.post(url, files=files, auth=auth, data=data)
            # TODO handle response and return JSON
            response.raise_for_status()
        except requests.HTTPError as error:
            logger.warning(f"Receiving pushed resource failed: {error.response.text}")
            return JsonResponse(status=500, data=error.response.text)
        except Exception as e:
            logging.error("unable to import pushed data", e)
            return JsonResponse(status=500, data=e)
        
        # TODO handle style

        # TODO handle thumbnail

        # TODO handle permissions
        
        # TODO handle groups and owner
        
        # TODO handle keywords, licenses, ... actually the whole resource file
        
        # TODO if relevant: persist / override sidecar files
        subtype = resource.subtype
        if subtype == "vector":
            
            # TODO prepare GeoJSON import

            pass
        elif subtype == "raster":
            # TODO prepare raster import

            pass
        else:
            return JsonResponse(status=500, data={
                "error": f"Cannot handle subtype {subtype}"
            })



def _get_api_serializer(app) -> BaseDynamicModelSerializer:
    if app:
        try:
            _module = importlib.import_module(f"{app.name}.api.serializers")
            for name, obj in inspect.getmembers(_module):
                if inspect.isclass(obj) and issubclass(obj, ResourceBaseSerializer) and not "List" in obj.__name__:
                    return obj
        except Exception as e:
            logger.debug(e)
    return ResourceBaseSerializer


def _resolve_type_serializer(resource_type: str = None) -> typing.Tuple[object, BaseDynamicModelSerializer]:
    _resource_type = ResourceBase
    _serializer = ResourceBaseSerializer
    if resource_type:
        _resource_type_found = False
        for label, app in apps.app_configs.items():
            if _resource_type_found:
                break
            if hasattr(app, "models"):
                for _model_name, _model in app.models.items():
                    if resource_type.lower() == _model_name.lower():
                        _resource_type_found = True
                        _serializer = _get_api_serializer(app)
                        _resource_type = _model
                        break
        if not _resource_type_found:
            _resource_type = ResourceBase
    return _resource_type, _serializer
