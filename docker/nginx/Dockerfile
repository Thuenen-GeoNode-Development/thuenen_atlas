ARG BASE_IMAGE_VERSION
FROM 52north/geonode-nginx:${BASE_IMAGE_VERSION}

COPY ./cert.pem /geonode-certificates/autoissued/fullchain.pem
COPY ./key.pem /geonode-certificates/autoissued/privkey.pem
