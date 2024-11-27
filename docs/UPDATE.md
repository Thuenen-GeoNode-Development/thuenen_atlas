# Update Thuenen Atlas

WIP


MapStore2
 - merge upstream

geonode-mapstore-client
 - merge upstream
 - git submodule update --remote
 - do merge, but skip geonode_mapstore_client/static/mapstore/dist
 - after merge: git reset dist folder -> git clean dist folder -> restore dist folder
 - push for workflow build and merge PR after that
 - 

geonode
 - merge upstream
 - 
 
 
thuenen_atlas
 - merge upstream (blueprint)
 - adjust versions for datapackage and externalapplications
 - git submodule update --remote
 - 
 
datapackage
 - align with geonode-dev-datapackage

externalapplications
 - contrib_externalapplications/