#!/bin/bash

global_config="$GEOSERVER_DATA_DIR/global.xml"

# strip trailing slash
sed -i "s|.*<proxyBaseUrl>.*|<proxyBaseUrl>${SITEURL}geoserver</proxyBaseUrl>|" $global_config

/usr/local/tomcat/tmp/entrypoint.sh