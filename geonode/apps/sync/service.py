import logging
from geonode.base.models import ResourceBase
from .models import RemoteGeoNodeInstance

logger = logging.getLogger("geonode.push_to_remote")


def push_to_remote(resource: ResourceBase, remote: RemoteGeoNodeInstance, force: bool = False):
    logger.info("Pushing %s to %s (force=%s)", resource, remote, force)
