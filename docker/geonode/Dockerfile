ARG BASE_IMAGE_VERSION
FROM 52north/geonode_thuenen:${BASE_IMAGE_VERSION}

COPY ./geonode-mapstore-client /usr/src/django_geonode_mapstore_client
RUN yes w | pip install -e /usr/src/django_geonode_mapstore_client

COPY ./ldap /usr/src/ldap
RUN yes w | pip install -e /usr/src/ldap

COPY ./requirements.txt more_requirements.txt
RUN yes w | pip install --src /usr/src -r more_requirements.txt

RUN rm .env*
