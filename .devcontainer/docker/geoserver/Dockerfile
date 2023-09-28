ARG BASE_IMAGE_VERSION
FROM 52north/geonode-geoserver:${BASE_IMAGE_VERSION}

ENV GEOSERVER_DATA_DIR="/geoserver_data/data"

# adjust geonode2-oauth config for devcontainer setup 
COPY ./adjust-oauth-config.sh /adjust-oauth-config.sh
RUN chmod +x /adjust-oauth-config.sh

VOLUME $GEOSERVER_DATA_DIR
ENTRYPOINT [ "/adjust-oauth-config.sh" ]
