ARG BASE_IMAGE_VERSION
#FROM geonode/nginx:${BASE_IMAGE_VERSION}
FROM geonode/nginx:1.25.3-v1

COPY ./cert.pem /geonode-certificates/autoissued/fullchain.pem
COPY ./key.pem /geonode-certificates/autoissued/privkey.pem

# overwrite nginx conf for hardening
COPY ./nginx.https.available.conf.envsubst /etc/nginx/nginx.https.available.conf.envsubst
