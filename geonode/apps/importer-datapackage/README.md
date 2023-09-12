# Datapackage Support for geonode-importer

This module provides a datapackage handler for the geonode-importer.
The handler leverages the OGR VRT format to import layers described in a tabular data resource schema.
To make this possible a schema mapping takes place. 

The project is still a prototype and only a minimal set of possible features are supported.

## Installation

The module can be installed as normal python module. 
Once installed, the handler can be configured similary to the normal handlers provided by the geonode-importer.

Note: At the time of writing, the geonode-importer is expected to relax assumptions on the layer import.
Those are available under https://github.com/Thuenen-52North-Erweiterung-GeoNode:geonode-importer:allow-nonspatial-layer-import and hopefully merged to upstream.

## Upload

A datapackage can be uploaded as ZIP-file.
In the ZIP-file a `datapackage.json` is expected to be found, along with any other file referenced from the `datapackage.json`.
At the moment only CSV-files were tested.

## Limitations

- no fancy formats or regexes
- primary keys are imported without any database constraints
- ...