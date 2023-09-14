# Thünen Atlas, GeoNode Instance 

This document will guide you through the development setup of the Thünen Atlas which is based on [GeoNode](https://geonode.org/), a spatial content management system.
The needed components are available as [Docker](https://www.docker.com/) base images and will be customized and set up and run via the [docker-compose](https://docs.docker.com/compose/) tool.

## Component Overview

Here is a short overview of the installed components and how they are connected.

![GeoNode Architecture](./docs/geonode_architecture_4x.png "Geonode Architecture")

The components are:

- **Django:** The actual GeoNode component.
It exposes a [pyCSW API](https://pycsw.org/) and the GeoNode API.
- **Celery:** [Celery](https://docs.celeryq.dev/en/stable/) forms the asynchronuous task queue of GeoNode.
- **GeoServer:** [GeoServer](https://geoserver.org/) is the backend server of GeoNode for sharing geospatial data.
It exposes OGC APIs such as WMS, WFS, etc. 
- **Nginx:** [Nginx](https://nginx.com) serves as advanced load balancer, web server and reverse proxy to all GeoNode components.
- **PostgreSQL:** GeoNode and GeoServer are using [PostgreSQL](https://www.postgresql.org)  with the geospatial extension [PostGIS](https://postgis.net) as the database.


## Thünen Specific Repositories

Thünen Atlas maintains own repositories holding all code changes, fixes, and adjustments which are not (yet) part of [GeoNode upstream](https://github.com/geonode/geonode) and related projects as genonde-mapstore-client.

Most important repositories are

* **thuenen_atlas**: The [thuenen_atlas repository](https://github.com/Thuenen-GeoNode-Development/thuenen_atlas) assembles all components and provides the development setup
* **GeoNode**: A [fork of GeoNode](https://github.com/Thuenen-GeoNode-Development/geonode) holding code changes not (yet) merged with upstream.
* **geonode-mapstore-client**: A [fork of geonode-mapstore-client](https://github.com/Thuenen-GeoNode-Development/geonode-mapstore-client) which holds UI adjustments not (yet) merged with upstream. 
* **MapStore2**: A [fork of MapStore2](https://github.com/Thuenen-GeoNode-Development/MapStore2) holding code changes not (yet) merged with upstream.
* **Apps and Extensions**:
  * **externalapplications**: The [externalapplications app](https://github.com/GeoNodeUserGroup-DE/contrib_externalapplications) is a GeoNode contrib app which adds external applications as new resource_type.
  * **atlas**: The atlas app, currently part of [Thünen Atlas repository](https://github.com/Thuenen-GeoNode-Development/thuenen_atlas), adds template pages for which an admin can add curated content to.
  * **importer-datapackage**: [A python module](https://github.com/GeoNodeUserGroup-DE/importer-datapackage) which adds a non-spatial data handler for [the geonode-importer](https://github.com/geononde/geonode-importer).

 Main goal of all forks is, to stay as close to the upstream as possible.
 Some repositories are maintained in a repository of the [German GeoNode user group](https://github.com/GeoNodeUserGroup-DE).
## Development Structure



### Quick Start

### DevContainers

### Docker Images Origins

