ARG BASE_IMAGE_VERSION
#FROM geonode/geoserver_data:${BASE_IMAGE_VERSION}
FROM geonode/geoserver_data:2.24.2-v2

# configure logging
RUN sed 's|<stdOutLogging>false</stdOutLogging>|<stdOutLogging>true</stdOutLogging>|' -i "/geoserver_data/data/logging.xml"
