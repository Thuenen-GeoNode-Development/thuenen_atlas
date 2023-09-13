ARG BASE_IMAGE_VERSION
FROM 52north/geonode_thuenen:${BASE_IMAGE_VERSION}

COPY ./geonode-mapstore-client /usr/src/geonode-mapstore-client
RUN yes w | pip install -e /usr/src/geonode-mapstore-client

COPY ./requirements.txt more_requirements.txt
RUN yes w | pip install --src /usr/src -r more_requirements.txt


