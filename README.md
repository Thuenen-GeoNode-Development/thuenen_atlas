# Thuenen_Atlas

## Project Genesis

This GeoNode project was generated via the [official GeoNode template v4.0.x](https://github.com/GeoNode/geonode-project). To create this project we followed the steps:

```sh
git clone https://github.com/GeoNode/geonode-project.git -b 4.0.x
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3 thuenen
# Prompt gets prefixed with the active environment
(thuenen) pip install Django==3.2.16
(thuenen) django-admin startproject --template=./geonode-project -e py,sh,md,rst,json,yml,ini,env,sample,properties -n monitoring-cron -n Dockerfile thuenen_atlas
```

The created project is tracked under git version control: https://github.com/Thuenen-52North-Erweiterung-GeoNode/thuenen_atlas

## Project Customization

The thuenen_Atlas project integrates different customizations which are tracked at

- https://github.com/Thuenen-52North-Erweiterung-GeoNode/geonode-contribs
- https://github.com/Thuenen-52North-Erweiterung-GeoNode/geonode-mapstore-client.git

If a newer version of a contrib module needs to be integrated, the Docker build has to be repeated as the
contrib modules have to be resolved at build time.

## Building the project

Create a `.env` file that configures the services. You can copy from the sample:

```sh
$ cp .env.sample .env
```

Build and run:

```sh
# the build will take quite a while
docker-compose build
# start geonode detached
docker-compose up -d
# once running you can follow the logs
docker-compose logs -f
```

An update can be done on running containers:

```sh
# Re-build the GeoNode Container
docker-compose build django --no-cache
# Restart will pick the fresh image
docker-compose up -d --force-recreate django celery
```

## Using the Instance

Open http://localhost in your favorite browser.

The default admin login is `admin:admin`.

## Useful Docker Commands

Stop all containers of the `thuenen_atlas` setup:

```sh
# either via docker compose
docker-compose down
# or directly via docker
docker stop $(docker ps -a --filter name=thuenen_atlas --format={{.Names}})
```

Remove all volumes of the `thuenen_atlas` setup:

```sh
docker volume rm $(docker volume ls --filter="name=thuenen_atlas" --format={{.Name}})
```
