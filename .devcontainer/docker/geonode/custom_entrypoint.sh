#!/bin/bash


oauth_config="/geoserver_data/data/security/filter/geonode-oauth2/config.xml"
redirect_uri="${GEOSERVER_PUBLIC_LOCATION}"geoserver/index.html

sed -i "s|<redirectUri>.*</redirectUri>|<redirectUri>$redirect_uri</redirectUri>|g" $oauth_config

./entrypoint.sh sleep infinity