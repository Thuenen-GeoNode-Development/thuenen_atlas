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
## Development



### Quick Start

Clone the repository.

```sh
git clone https://github.com/Thuenen-GeoNode-Development/thuenen_atlas -b thuenen_4.x
cd thuenen_4.x
```

> :bulb: **Note**
>
> `geonode-mapstore-client` is a huge repository.
> If you want to keep a small footprint, add `--shallow-submodules --recurse-submodules` when cloning the repository.

To build and start GeoNode, run:

```sh
docker-compose up -d --build 
```

You can follow the logs: `docker-compose logs -f <optional-service-name>`.


To shutdown GeoNode, run:

```sh
docker-compose down
```

To remove all volumes you have to append the `-v` flag.


### DevContainers

If you are using vs-code as an IDE you can start [the devcontainer setup](https://containers.dev/).

Make sure, you have installed the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
Build and open the devcontainer and wait until everything has started.
After downloading and building the images, the terminal prints when containers are starting:

```sh
... # cut for brevity

[188981 ms] Start: Run: docker-compose --project-name geonode -f /home/ridoo/data/coding/projects/thuenen-atlas/thuenen_atlas/docker-compose.yml -f /home/ridoo/data/coding/projects/thuenen-atlas/thuenen_atlas/.devcontainer/docker-compose.yml -f /home/ridoo/.config/Code - Insiders/User/globalStorage/ms-vscode-remote.remote-containers/data/docker-compose/docker-compose.devcontainer.build-1694764280181.yml -f /home/ridoo/.config/Code - Insiders/User/globalStorage/ms-vscode-remote.remote-containers/data/docker-compose/docker-compose.devcontainer.containerFeatures-1694764463670.yml up -d
[+] Running 16/16
 ✔ Network geonode_default          Created                                0.2s 
 ✔ Volume "geonode-gsdatadir"       Create...                              0.0s 
 ✔ Volume "geonode-backup-restore"  C...                                   0.0s 
 ✔ Volume "geonode-statics"         Created                                0.0s 
 ✔ Volume "geonode-dbbackups"       Create...                              0.0s 
 ✔ Volume "geonode-dbdata"          Created                                0.0s 
 ✔ Volume "geonode-data"            Created                                0.0s 
 ✔ Volume "geonode-rabbitmq"        Created                                0.0s 
 ✔ Volume "geonode-tmp"             Created                                0.0s 
 ✔ Container gsconf4geonode         Started                                0.1s 
 ✔ Container nginx4geonode          Started                                0.1s 
 ✔ Container db4geonode             Started                                0.1s 
 ✔ Container rabbitmq4geonode       Starte...                              0.1s 
 ✔ Container geoserver4geonode      Creat...                               0.1s 
 ✔ Container django4geonode         Created                                0.0s 
 ✔ Container celery4geonode         Created                                0.0s
```

When seeing the about output, you can watch logging via `docker-compose logs -f`.

The devcontainer setup does not start GeoNode automatically.
Once the container is ready, you can press `F5` to start debugging GeoNode.


> :bulb: **Note**
>
> In the devcontainer setup, routing is not done through nginx!
> Starting GeoNode in devcontainer actually runs `python manage.py runserver` which starts a lightweight development web server based on WSGI.



### Develop GeoNode UI

The GeoNode UI is written in ReactJS and uses components from the MapStore2 Web framework.
As GeoNode is a Django project, integration of the UI works as a django app.
This django app is implemented by the `geonode-mapstore-client` project.
At the moment, Thünen Atlas also provides [an own fork for UI adjustments](https://github.com/Thuenen-GeoNode-Development/geonode-mapstore-client).


The UI is a single page application and (mostly) communicates with GeoNode via API.
There are exceptions where (still) Django templates are used.

To start developing the UI, you can [follow the official development guide](https://github.com/geosolutions-it/geonode-mapstore-client/blob/master/docs/development.md).

In devcontainer setup, the vs-code debug launcher [opens port `8001` for HTTP connections](https://github.com/Thuenen-GeoNode-Development/geonode/blob/thuenen_4.x/uwsgi.ini#L3).
Configure that port in your `./geonode_mapstore_client/client/.env` file:

```sh
DEV_SERVER_PROTOCOL=http
DEV_SERVER_HOSTNAME=localhost
DEV_TARGET_GEONODE_HOST=localhost:8001
```

Then build and start the client:

```sh
cd ./geonode_mapstore_client/client
npm install
npm start
```

Make sure to use node version `12.x` (e.g. via `nvm`).

## Docker Images

All images are based on pre-built base images.
This ensure more performant builds regarding to time and size.
Docker provides concepts to extend and adjust the setup, for example via volume mounts, or building atop of those images.


> :bulb: **Base Images**
>
> As for today, tags of official GeoNode images are not as stable as we would expect from an upstream project.
> Therefore, we rely on images built from [the `52north/geonode` fork](https://github.com/52north/geonode/tree/52n-master) of GeoNode upstream.
> This way, we can track upstream changes (to stay close to the upstream) and guarantee stable tags at the same time.
>
> However, as said before, Thünen Atlas has unmerged changes on GeoNode core, and uses a project specific image which is built from [a project specific fork of GeoNode](https://github.com/Thuenen-GeoNode-Development/geonode).


The project prepares `Dockerfile`s for each component to allow a well-defined extension structure:

```sh
docker
├── geonode                         # Extension point for GeoNode
│   ├── Dockerfile                  # Uses 52north/geonode_thuenen
│   ├── geonode-mapstore-client     # Submodule for the GeoNode UI
│   └── requirements.txt            # Further packages to install
├── geoserver                       # Extension point for GeoServer
│   └── Dockerfile                  # Uses 52north/geonode-geoserver
├── geoserver_data                  # Extension point for GeoServer data dir
│   └── Dockerfile                  # Uses geonode/geonode_data (may change when tagging becomes unstable as well)
├── nginx                           # Extension point for Nginx
│   └── Dockerfile                  # Uses geonode/geonode-nginx
└── postgresql                      # Extension point for Postgres
    └── Dockerfile                  # Uses geonode/postgis (may change when tagging becomes unstable as well)
```
