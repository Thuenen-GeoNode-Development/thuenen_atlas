import os
import json
import time
import typing
import inspect
import logging
import requests
import importlib

from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.apps import apps

from geonode.base.models import ResourceBase
from geonode.resource.manager import resource_manager
from geonode.resource.models import ExecutionRequest
from geonode.layers.api.serializers import (
    AttributeSerializer,
    StyleSerializer,
)
from geonode.base.api.serializers import (
    BaseDynamicModelSerializer,
    GroupSerializer,
    LicenseSerializer,
    ResourceBaseSerializer,
    RestrictionCodeTypeSerializer,
    SimpleHierarchicalKeywordSerializer,
    SimpleRegionSerializer,
    SimpleThesaurusKeywordSerializer,
    SimpleTopicCategorySerializer,
    UserSerializer,
)

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import authentication
from rest_framework import permissions
from oauth2_provider.contrib import rest_framework

from ..apps import BASE_FILE, XML_FILE, DATA_FILE, STYLE_FILE, THUMBNAIL_FILE
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
        pushed_resource = json.load(request.FILES[BASE_FILE])
        model, serializer = _resolve_type_serializer(pushed_resource["resource_type"])

        # XXX no valid deserialization plus data is missing
        # sync_serializer = create_serializer(model)
        # data = sync_serializer(pushed_resource)

        # TODO Write De-Serializer (analogue to pushing side) (ignore id)
        # TODO check if related objects exist already -> replace with db id
        # TODO Linked documents -> push with resource
        # TODO use UUIDs or unique fields instead of db ids

        # test criteria
        #
        # - accessible only for admin
        # - unless force=True existing datasets will not be overridden
        # - geonode-importer is used
        #
        # - works for raster and vector
        # - handles / overrides sidecar files
        # - handles style and thumbnail files

        #### workflow:
        ## https://private-user-images.githubusercontent.com/6172324/283863097-20a834f6-7d9f-454c-a06d-65289d7a814d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDM3NzQwMTQsIm5iZiI6MTcwMzc3MzcxNCwicGF0aCI6Ii82MTcyMzI0LzI4Mzg2MzA5Ny0yMGE4MzRmNi03ZDlmLTQ1NGMtYTA2ZC02NTI4OWQ3YTgxNGQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQUlXTkpZQVg0Q1NWRUg1M0ElMkYyMDIzMTIyOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyMzEyMjhUMTQyODM0WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZTgyNGE4NmUyNjYzMDk1ZmQyNzllMWRkYWMyYWQxYmNmNDM3ZDg2NGEzMTJlOTM2Yzk0MTM3ZjJmOWRmNzNmOSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.tKGZCspiRK2agSKWkoQFgagg8nYAN3k0b0q2PeLz3-0

        ####
        ## handle "is UUID present in remote node?"
        uuid = request.data["uuid"]
        force = request.data["force"]
        resources_exists = ResourceBase.objects.filter(uuid=uuid).exists()
        if resources_exists and force == "False":
            return JsonResponse(status=400, data={"error": f"Resource {uuid} exists and force is not true!"})

        ####
        ## handle "Does resource belong to a group??
        if hasattr(pushed_resource, "group"):
            group = GroupSerializer(data=pushed_resource["group"])

            ## handle "is group & group categories present at remote node?"
            # XXX group vs groupprofile
            # exists via name?
            # no categories!

        ####
        ## handle "check if owner/metadata contacts are present in remote node"
        # TODO create users
        # XXX LDAP tagging user?! -> eike

        strip_values = ["resourcebase_ptr"]
        [pushed_resource.pop(to_strip, None) for to_strip in strip_values]
        s = create_serializer(model)(data=pushed_resource)
        try:
            dataset = model.objects.get(uuid=pushed_resource.get("uuid"))
            s.update(dataset, pushed_resource) + model._meta.many_to_many
        except model.DoesNotExist:
            s.create(pushed_resource)

        if hasattr(pushed_resource, "poc"):
            poc = UserSerializer(pushed_resource["poc"])
        if hasattr(pushed_resource, "metadata_author"):
            metadata_author = UserSerializer(pushed_resource["metadata_author"])

        license = LicenseSerializer(data=pushed_resource["license"])
        category = SimpleTopicCategorySerializer(data=pushed_resource["category"])
        restriction_code_type = RestrictionCodeTypeSerializer(data=pushed_resource["restriction_code_type"])
        default_style = StyleSerializer(data=pushed_resource["default_style"])
        # XXX
        featureinfo_custom_template = pushed_resource["featureinfo_custom_template"]

        # many relations
        styles = StyleSerializer(data=pushed_resource["styles"], many=True)
        keywords = SimpleHierarchicalKeywordSerializer(data=pushed_resource["keywords"], many=True)
        tkeywords = SimpleThesaurusKeywordSerializer(data=pushed_resource["tkeywords"], many=True)
        attribute_set = AttributeSerializer(data=pushed_resource["attribute_set"], many=True)
        regions = SimpleRegionSerializer(data=pushed_resource["regions"], many=True)

        # XXX serialized during representation
        # links = pushed_resource["links"]
        # perms = pushed_resource["perms"]
        # remote_service

        def continue_after_import(execution_id):
            req = ExecutionRequest.objects.filter(exec_id=execution_id)
            status = req.get().status
            if status == ExecutionRequest.STATUS_FINISHED:
                #### Copy metadata
                #### Copy style
                #### Copy feature catalogue / attribute descriptions
                #### update permissions
                #### linked datasets available

                values = {}
                kwargs = {regions: regions, keywords: keywords}

                # TODO handle style
                if hasattr(request.FILES, STYLE_FILE):
                    style_file = request.FILES[STYLE_FILE]
                    kwargs["sld_file"] = style_file

                # TODO handle thumbnail
                if hasattr(request.FILES, THUMBNAIL_FILE):
                    thumbnail_file = request.FILES[THUMBNAIL_FILE]
                    resource_manager.set_thumbnail(uuid=uuid, thumbnail=thumbnail_file)

                # TODO handle xml metadata
                if pushed_resource["metadata_uploaded"] and hasattr(request.FILES, XML_FILE):
                    xml_file = request.FILES[XML_FILE]

                resource_manager.update(uuid=uuid, vals=values, **kwargs)

                # TODO handle permissions

                # TODO handle groups and owner

                # TODO handle keywords, licenses, ... actually the whole resource file

                # TODO if relevant: persist / override sidecar files
                subtype = pushed_resource["subtype"]
                if subtype == "vector":
                    # TODO prepare GeoJSON import

                    pass
                elif subtype == "raster":
                    # TODO prepare raster import

                    pass
                else:
                    return JsonResponse(status=500, data={"error": f"Cannot handle subtype {subtype}"})

                return JsonResponse(
                    status=201, data={}, headers={"Location": f"{settings.SITEURL}catalogue/uuid/{uuid}"}
                )
            else:
                return JsonResponse(status=500, data={"error": "Handling pushed resource after importing data failed!"})

        try:
            response = _import_resource(
                request,
                data={
                    "uuid": uuid,
                    "overwrite_existing_layer": force,
                },
            )

            payload = json.loads(response.content.decode("utf-8"))
            execution_id = payload["execution_id"]

            req = ExecutionRequest.objects.get(exec_id=execution_id)
            while req.status.lower() in ["ready", "running"]:
                # TODO limit wait for completion

                # TODO setting how long import can take?
                # TODO check for failed import?

                time.sleep(5)
                req.refresh_from_db()

            return continue_after_import(execution_id)

        except requests.HTTPError as error:
            logger.exception(f"Importing pushed data failed: {error.response.text}")
            return JsonResponse(status=500, data=error.response.text)
        except Exception as e:
            logging.exception("Importing pushed data failed", e)
            return JsonResponse(status=500, data=e)


def _import_resource(request, data):
    """delegates import to geonode-importer"""
    data_file = request.FILES[DATA_FILE]
    files = {
        "base_file": (data_file.name, data_file, data_file.content_type),
    }

    try:
        auth = (os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))
        url = f"{settings.SITEURL}api/v2/uploads/upload"
        # TODO remove webhook.site
        # url = "https://webhook.site/20feca89-00f7-4d8b-943f-df7f20a6c901"
        response = requests.post(url, files=files, auth=auth, data=data)
        response.raise_for_status()
    except requests.HTTPError as error:
        logger.warning(f"Receiving pushed resource failed: {error.response.text}")
        return JsonResponse(status=500, data=error.response.text)
    except Exception as e:
        logging.error("unable to import pushed data", e)
        return JsonResponse(status=500, data=e)


def _create_or_update_user(user):
    # strip invalid attributes
    user.pop("pk", None)

    data = UserSerializer(data=user)
    query = {"username": user.get("username")}

    # FIXME generalize into serializers which recursively iterate through related fields?

    try:
        # update existing user
        model = data.get_model()
        entry = model.objects.get(**query)
        saved_user = data.update(entry, user)
    except Model.DoesNotExist:
        # create new user
        data.is_valid(raise_exception=True)
        saved_user = data.save()

    return saved_user


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
