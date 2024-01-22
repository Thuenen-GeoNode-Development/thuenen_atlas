import sys
import logging

from django.contrib.gis.db.models import GeometryField
from django.contrib.auth.models import Group
from django.db.models.fields.related import RelatedField, ManyToManyField, OneToOneField, ForeignKey
from django.db.models import Model

from dynamic_rest.serializers import DynamicModelSerializer, DynamicRelationField
from rest_framework.utils import html, model_meta, representation
from rest_framework.fields import (  # NOQA # isort:skip
    CreateOnlyDefault, CurrentUserDefault, SkipField, empty
)
from rest_framework_gis.fields import GeometryField as GeometrySerializer
from taggit.managers import TaggableManager

from geonode.settings import DEBUG
from geonode.base.models import _HierarchicalTagManager
from geonode.people.models import Profile
from geonode.base.models import License
from geonode.layers.models import Attribute, Dataset
from geonode.layers.api.serializers import AttributeSerializer, DatasetSerializer
from geonode.base.api.serializers import HierarchicalKeywordSerializer, ThesaurusKeywordSerializer

# dynamically define serializers in this module
module = sys.modules[__name__]
logger = logging.getLogger(__name__)

setattr(module, "HierarchicalKeywordSerializer", HierarchicalKeywordSerializer)
setattr(module, "ThesaurusKeywordSerializer", ThesaurusKeywordSerializer)


def _get_or_raise(model, query):
    try:
        # expect existing entity
        return model.objects.get(**query)
    except model.DoesNotExist as e:
        logger.exception(f"{model} must be created by the pushing instance!", e)


def _setattrs(_self, **kwargs):
    for k, v in kwargs.items():
        setattr(_self, k, v)


def _create_or_update(data, model, query, strip_values=["pk"]):
    # strip values which are not relevant (e.g. pk from a foreign db)
    [data.pop(to_strip, None) for to_strip in strip_values]

    try:
        # update existing entity
        entry = model.objects.get(**query)
        _setattrs(entry, **data)
        entry.save()
    except model.DoesNotExist:
        # create new entity
        saved_entity = model.objects.save(data)
    except model.MultipleObjectsReturned:
        logger.exception("cannot update object because aof an ambigious query!")
        raise

    return saved_entity


class NestedWriteMixin:
    
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
    
    def create(self, validated_data):
        
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        data = self.save_nested(validated_data, ModelClass)
        instance = ModelClass.objects.create(**data)
        
        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        
        super().update(instance, validated_data)

    def save_nested(self, data, model):
        """
        Saves or updates all related fields

        Makes sure that each (embedded) relation is replaced by an
        appropriate pk instead.
        """

        for field in model._meta.fields:
            if field.name in data:
                if isinstance(field, GeometryField) and data[field.name]:
                    model = field.related_model
                    geom = GeometrySerializer()
                    data[field.name] = geom.to_internal_value(data[field.name])

                elif isinstance(field, RelatedField):
                    model = field.related_model
                    if model == Profile and data[field.name]:
                        profile = data.pop(field.name)
                        try:
                            query = {"username": profile.get("username")}
                            data[field.name + "_id"] = model.objects.get(**query).pk
                        except model.DoesNotExist:
                            saved_profile = create_serializer(model)(data=profile)
                            data[field.name + "_id"] = saved_profile.pk
                            
                    if model == License and data[field.name]:
                        license = data.pop(field.name)
                        try:
                            query = {"name": license.get("name")}
                            data[field.name + "_id"] = model.objects.get(**query).pk
                        except model.DoesNotExist:
                            saved_license = create_serializer(model)(data=license)
                            data[field.name + "_id"] = saved_license.pk

                    if model == Group and data[field.name]:
                        group = data.pop(field.name)
                        query = {"name": group.get("name")}
                        data[field.name + "_id"] = _get_or_raise(model, query).pk
                        
                        # if field.many_to_many or field.one_to_many:
                        #     data.set(field.name, [get_group(group) for group in data[field.name]])
                        # else:

        return data


class _SerializerFactory:
    FIELD_BLACK_LIST = {
        "Profile": ["password"],
        "Document": [
            "resourcebase_ptr",
            "csw_anytext",  # FIXME remove
            "metadata_xml",  # FIXME remove
        ],
    }

    def __init__(self):
        self.creating = set()

    def create(self, m):
        polymorphic_ctype_fields = getattr(m, "polymorphic_internal_model_fields", [])

        def get_serializer_name(m):
            return f"{m.__name__}Serializer"

        def include(field):
            ignored_fields = self.FIELD_BLACK_LIST.get(m.__name__, [])
            return field.name not in ignored_fields and field.name not in polymorphic_ctype_fields

        name = get_serializer_name(m)
        if name in self.creating:
            # do not run into a recursion
            return f"{__name__}.{name}"
        elif name not in dir(module) or DEBUG:
            self.creating.add(name)
            print(f"defining {__name__}.{name}")
            logger.info(f"defining {__name__}.{name}")
            class_dict = {}

            class Meta:
                model = m
                name = str(m)
                fields = [field.name for field in m._meta.fields if include(field)] + [
                    field.name for field in m._meta.many_to_many if include(field)
                ]

            if hasattr(m, "attributes"):
                Meta.fields.append("attribute_set")
                class_dict["attribute_set"] = DynamicRelationField(AttributeSerializer, embed=True, many=True)

            class_dict["Meta"] = Meta

            for field in m._meta.fields + m._meta.many_to_many:
                if include(field):
                    if isinstance(field, GeometryField):
                        class_dict[field.name] = GeometrySerializer(required=False)
                    elif isinstance(field, RelatedField):
                        class_dict[field.name] = DynamicRelationField(
                            self.create(field.related_model), embed=True, many=field.many_to_many or field.one_to_many
                        )
                    elif isinstance(field, _HierarchicalTagManager):
                        class_dict[field.name] = DynamicRelationField(
                            self.create(field.related_model), embed=True, many=True
                        )

            setattr(
                module,
                name,
                type(
                    name,
                    (
                        NestedWriteMixin,
                        DynamicModelSerializer,
                    ),
                    class_dict,
                ),
            )
            self.creating.remove(name)

        return getattr(module, name)


_serializerFactory = _SerializerFactory()
create_serializer = _serializerFactory.create


def test():
    from sync.models import RemotePushJob

    job = RemotePushJob.objects.first()
    resource = job.resource.polymorphic_ctype.get_object_for_this_type(pk=job.resource.pk)
    print(resource_to_json(resource))


def resource_to_json(resource):
    import json
    from sync.serializers import create_serializer
    from django.core.serializers.json import DjangoJSONEncoder

    Serializer = create_serializer(resource._meta.model)
    serializer = Serializer()
    representation = serializer.to_representation(resource)
    return json.dumps(representation, cls=DjangoJSONEncoder)


def test2():
    import json
    from sync.models import RemotePushJob
    from geonode.storage.manager import StorageManager
    import requests
    from io import StringIO

    job = RemotePushJob.objects.first()
    resource = job.resource.polymorphic_ctype.get_object_for_this_type(pk=job.resource.pk)
    sm = StorageManager()

    files = files = {
        "resource": ("resource.json", StringIO(resource_to_json(resource)), "application/json"),
        "thumbnail_path": (resource.thumbnail_path, sm.open(resource.thumbnail_path)),
    }
    if resource.files:
        for idx, path in enumerate(resource.files):
            files[f"files[{idx}]"] = sm.open(path)

    if resource.thumbnail_path:
        requests.post("https://webhook.site/6c2f556d-52cb-4211-8b98-555d2baf80c5", files=files)
