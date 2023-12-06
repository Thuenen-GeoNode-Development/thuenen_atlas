from dynamic_rest.serializers import DynamicModelSerializer, DynamicRelationField
from django.db.models.fields.related import RelatedField, ManyToManyField, OneToOneField, ForeignKey
from rest_framework_gis.fields import GeometryField as GeometrySerializer
from django.contrib.gis.db.models import GeometryField
from geonode.base.models import _HierarchicalTagManager
from geonode.base.api.serializers import (
    HierarchicalKeywordSerializer,
    ThesaurusKeywordSerializer
)
from taggit.managers import TaggableManager
import logging
import sys
# dynamically define serializers in this module
module = sys.modules[__name__]
logger = logging.getLogger(__name__)

setattr(module, "HierarchicalKeywordSerializer", HierarchicalKeywordSerializer)
setattr(module, "ThesaurusKeywordSerializer", ThesaurusKeywordSerializer)

FIELD_BLACK_LIST = {
    "Profile": [ "password" ],
    "Document": [ 
        "polymorphic_ctype", 
        "resourcebase_ptr",
        "csw_anytext", # FIXME remove
        "metadata_xml", # FIXME remove
    ]
}


class _SerializerFactory():
    def __init__(self):
        self.creating = set()

    def create(self, m):
        
        def get_serializer_name(m):
            return f"{m.__name__}Serializer"
        def include(field):
            return field.name not in FIELD_BLACK_LIST.get(m.__name__, [])

        name = get_serializer_name(m)
        if name in self.creating:
            # do not run into a recursion
            return f"{__name__}.{name}"
        elif name not in dir(module):
            self.creating.add(name)
            print(f"defining {__name__}.{name}")
            logger.info(f"defining {__name__}.{name}")
            class_dict = {}

            class Meta():
                model = m
                name = str(m)
                fields = [
                    field.name 
                    for field in m._meta.fields 
                    if include(field)
                ] + [
                    field.name 
                    for field in m._meta.many_to_many
                    if include(field)
                ]            
            class_dict["Meta"] = Meta

            for field in m._meta.fields + m._meta.many_to_many:
                if include(field):
                    if isinstance(field, GeometryField):
                        class_dict[field.name] = GeometrySerializer(required=False)
                    elif isinstance(field, RelatedField):
                        class_dict[field.name] = DynamicRelationField(
                            self.create(field.related_model), 
                            embed=True,
                            many=field.many_to_many or field.one_to_many)
                    elif isinstance(field, _HierarchicalTagManager):
                        class_dict[field.name] = DynamicRelationField(
                                self.create(field.related_model), 
                                embed=True,
                                many=True)
                    
                      
            setattr(module, name, type(name, (DynamicModelSerializer,), class_dict))
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
    
    files = files={
            "resource": ("resource.json", StringIO(resource_to_json(resource)), "application/json"),
            "thumbnail_path": (resource.thumbnail_path, sm.open(resource.thumbnail_path)),
    }
    if resource.files:
        for idx, path in enumerate(resource.files):
            files[f"files[{idx}]"] = sm.open(path)
        

    if resource.thumbnail_path:
        requests.post("https://webhook.site/6c2f556d-52cb-4211-8b98-555d2baf80c5", files=files)
   