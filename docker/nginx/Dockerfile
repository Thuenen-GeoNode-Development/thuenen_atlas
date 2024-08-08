ARG BASE_IMAGE_VERSION
FROM geonode/nginx:${BASE_IMAGE_VERSION}

ENV STATIC_ROOT=/mnt/volumes/statics/static/
ENV MEDIA_ROOT=/mnt/volumes/statics/uploaded/

COPY ./cert.pem /geonode-certificates/autoissued/fullchain.pem
COPY ./key.pem /geonode-certificates/autoissued/privkey.pem

# overwrite nginx conf for hardening
COPY ./nginx.https.available.conf.envsubst /etc/nginx/nginx.https.available.conf.envsubst