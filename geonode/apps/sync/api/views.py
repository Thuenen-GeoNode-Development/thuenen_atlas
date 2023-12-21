import json
import logging
import requests

from django.http import HttpResponse, JsonResponse
from django.conf import settings

from geonode.base.models import ResourceBase
from geonode.resource.api.utils import resolve_type_serializer

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import authentication
from rest_framework import permissions
from oauth2_provider.contrib import rest_framework

from ..apps import BASE_FILE, DATA_FILE, STYLE_FILE, THUMBNAIL_FILE

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
        resources_exists = ResourceBase.objects.filter(uuid = uuid).exists()
        if resources_exists and request.data["force"] == "False":
            return JsonResponse(status=400, data={
                "error": f"Resource {uuid} exists and force is not true!"
            })
        
        resource_json = json.load(request.FILES[BASE_FILE])
        resource_type = resource_json["resource_type"]
        _resource_type, _serializer = resolve_type_serializer(resource_type)
        data = _serializer(data=resource_json)
        
        sync_serializer = create_serializer(data.get_model())
        data = sync_serializer(json.load(resource_json))
        
        data = {
            "uuid": request.data.uuid,
            # TODO check if flag works, otherwise we have to delete resource manually
            "overwrite_existing_layer": request.data.force,
        }
        
        # prepare importer "upload"
        data_file = request.FILES[DATA_FILE]
        style_file = request.FILES[STYLE_FILE]
        thumbnail_file = request.FILES[THUMBNAIL_FILE]
        files = {
            "base_file": (data_file.name, data_file.content_type),
            "thumbnail": (thumbnail_file.name, thumbnail_file.content_type),
            "style": (style_file.name, style_file.content_type)
        }
        
        try:
            auth = (settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
            # TODO do it on localhost?
            url = f"{settings.SITEURL}/api/v2/uploads/upload"
            # TODO remove webhook.site
            # url = "https://webhook.site/20feca89-00f7-4d8b-943f-df7f20a6c901"
            response = requests.post(url, files=files, auth=auth, data=data)
            
            # TODO handle response and return JSON
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

        return JsonResponse(resource)

