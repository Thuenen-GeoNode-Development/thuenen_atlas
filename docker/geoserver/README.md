# GeoServer Image

## Plugins

To include GeoServer plugins into the built image, download them first.

For example, download the plugins `netcdf` and `vectortiles` for GeoServer version `2.23.3` run: 

 ```sh
 chmod +x download_plugins.sh
 ./download_plugins.sh "2.23.3" "netcdf vectortiles"
 ```

> :warning: **Warning**
>
> Make sure you do store irretrievable data in that directory!
> The `./plugins` directory will be deleted before download starts.

