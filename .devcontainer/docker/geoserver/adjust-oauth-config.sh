#!/bin/bash

oauth_config="$GEOSERVER_DATA_DIR/security/filter/geonode-oauth2/config.xml"

sed -i "s|.*<accessTokenUri>.*|<accessTokenUri>http://172.17.0.1:8001/o/token/</accessTokenUri>|" $oauth_config
sed -i "s|.*<userAuthorizationUri>.*|<userAuthorizationUri>http://172.17.0.1:8001/o/authorize/</userAuthorizationUri>|" $oauth_config
sed -i "s|.*<redirectUri>.*|<redirectUri>http://172.17.0.1/geoserver/index.html</redirectUri>|" $oauth_config
sed -i "s|.*<checkTokenEndpointUrl>.*|<checkTokenEndpointUrl>http://172.17.0.1:8001/api/o/v4/tokeninfo/</checkTokenEndpointUrl>|" $oauth_config
sed -i "s|.*<logoutUri>.*|<logoutUri>http://172.17.0.1:8001/account/logout/</logoutUri>|" $oauth_config

/usr/local/tomcat/tmp/entrypoint.sh