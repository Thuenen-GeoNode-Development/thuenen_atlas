ARG BASE_IMAGE_VERSION
ARG GEONODE_LB_HOST_IP
FROM 52north/geonode_thuenen:${BASE_IMAGE_VERSION}

COPY ./geonode-mapstore-client /usr/src/django_geonode_mapstore_client
RUN yes w | pip install -e /usr/src/django_geonode_mapstore_client

RUN sed -i 's@"endpointV1": "/api",@"endpointV1": "http://${GEONODE_LB_HOST_IP}:${GEONODE_LB_PORT}/api",@' /usr/src/django_geonode_mapstore_client/geonode_mapstore_client/static/mapstore/configs/localConfig.json
RUN sed -i 's@"endpointV2": "/api/v2"@"endpointV2": "http://${GEONODE_LB_HOST_IP}:${GEONODE_LB_PORT}/api/v2"@' /usr/src/django_geonode_mapstore_client/geonode_mapstore_client/static/mapstore/configs/localConfig.json

COPY ./requirements.txt more_requirements.txt
RUN yes w | pip install --src /usr/src -r more_requirements.txt

RUN rm .env*
