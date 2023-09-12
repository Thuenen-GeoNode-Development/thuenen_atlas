# Thünen Config App

Holds configuration assets like templates, snippets, etc. for Thünen Atlas GeoNode instance.

> :bulb: **Why this module?**
>
> `geonode_mapstore_client` runs as contrib and ships Django assets like templates, snippets, etc.
> That module adds itself at the beginning of `TEMPLATES.DIRS` so all assets are found there at first.
> The `thuenen_app` intregrates configuration of several contrib modules, e.g. within the `_geonode_config.html` which has to take precedence over those defined in `geonode_mapstore_client`.
