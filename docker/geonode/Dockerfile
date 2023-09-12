ARG BASE_IMAGE_VERSION
FROM 52north/geonode_thuenen:${BASE_IMAGE_VERSION}

RUN yes w | pip install -e -e git+https://github.com/GeoNodeUserGroup-DE/importer-datapackage.git@#main#egg=importer_datapackage
