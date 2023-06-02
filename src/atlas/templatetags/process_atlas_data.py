from django import template

register = template.Library()

@register.simple_tag
def createResourceArrays(resource):
    maps = []
    documents = []
    datasets = []
    for obj in resource:
        if obj.resource_type == "map":
            maps.append(obj)
        if obj.resource_type == "dataset":
            datasets.append(obj)
        if obj.resource_type == "document":
            documents.append(obj)
    return {
        "maps": maps,
        "datasets": datasets,
        "documents": documents
    }
