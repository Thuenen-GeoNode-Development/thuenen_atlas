ARG BASE_IMAGE_VERSION
FROM 52north/geonode_thuenen:${BASE_IMAGE_VERSION}

COPY ./geonode-mapstore-client /usr/src/django_geonode_mapstore_client
RUN yes w | pip install -e /usr/src/django_geonode_mapstore_client

COPY ./ldap /usr/src/ldap
RUN yes w | pip install -e /usr/src/ldap

COPY ./requirements.txt more_requirements.txt
COPY ./pycsw_local_mappings.py /usr/src/geonode/geonode/catalogue/backends/pycsw_local_mappings.py
COPY ./pycsw_local.py /usr/src/geonode/geonode/catalogue/backends/pycsw_local.py
COPY ./pycsw_http.py /usr/src/geonode/geonode/catalogue/backends/pycsw_http.py
COPY ./generic.py /usr/src/geonode/geonode/catalogue/backends/generic.py
COPY ./settings.py /usr/src/geonode/geonode/settings.py
COPY ./utils.py /usr/src/geonode/geonode/base/utils.py
RUN yes w | pip install --src /usr/src -r more_requirements.txt

RUN rm .env*
