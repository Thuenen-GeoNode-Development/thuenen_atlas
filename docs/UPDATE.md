# Update Thuenen Atlas

This documentation is still work in progress, so please be cautious and think before action.
In any case, make a backup of everything relevant.

**Recommendation:** Exercise everything on a clean sandbox environment first.


## Repository Overview

GeoNode Docker Blueprint

- Serves as opinionated blueprint for GeoNode projects
  - track upstream changes
  - leverage docker and git features to adjust particular project requirements
  - see details: https://github.com/GeoNodeUserGroup-DE/geonode-blueprint-docker?tab=readme-ov-file#background 
- Serves as isolated feature development, e.g. datapackage, which involves multiple repositories
  - see also: https://github.com/GeoNodeUserGroup-DE/geonode-dev-datapackage

<pre>

             <a href="https://github.com/Thuenen-GeoNode-Development/thuenen_atlas">thuenen_atlas</a>
                   |
                   | upstream
                   v
   <a href="https://github.com/GeoNodeUserGroup-DE/geonode-blueprint-docker">usergroup/geonode-docker-blueprint</a>
                   ^
                   | upstream
                   |
    <a href="https://github.com/GeoNodeUserGroup-DE/geonode-dev-datapackage">usergroup/geonode-dev-datapackage</a>

</pre>

Use features of Git or Docker (compose) to integrate external apps:

<pre>

          <a href="https://github.com/GeoNodeUserGroup-DE/contrib_externalapplications/">usergroup/contrib_externalapplications</a>
                           ^
                           | submodule/volume 
                           |
                     <a href="https://github.com/Thuenen-GeoNode-Development/thuenen_atlas">thuenen_atlas</a>
                       |        |
  via requirements.txt |        | via requirements.txt
                       |        v
                       |     <a href="https://github.com/GeoNodeUserGroup-DE/contrib_datapackage">usergroup/contrib_datapackage</a>
                       v
            <a href="https://github.com/geosolutions-it/geonode-subsites">geosolutions/geonode-subsites</a>
</pre>

Thünen Atlas incorporates customized GeoNode components which lay in their own Git repository each tracking their core upstream repository.
Beyond the core repositories, Thünen Atlas also incorporates feature development which is spread over multiple GeoNode components (e.g. GeoNode, geonode-mapstore-client).
An example is the datapackage development for tabular data.

Such development is done isolated from Thünen Atlas in a separated development setup which bundles everything necessary in its own geonode blueprint project.
Updating features would require to merge changes from upstream core and upstream feature development.

<pre>


                   <a href="https://github.com/GeoNode/geonode">geonode/geonode</a>
                     ^         ^                                    
      upstream/4.4.x |         | upstream/4.4.x
                     |         |
                     |      <a href="https://github.com/Thuenen-GeoNode-Development/geonode">thuenen/geonode</a>
                     |         |
                     |         | usergroup/datapackage_tabular-data
                     |         v 
                  <a href="https://github.com/GeoNodeUserGroup-DE/geonode">usergroup/geonode</a>


            <a href="https://github.com/GeoNode/geonode">geonode/geonode-mapstore-client</a>
                  ^                  ^
   upstream/4.4.x |                  | upstream/4.4.x
                  |                  |
                  |       <a href="https://github.com/Thuenen-GeoNode-Development/geonode-mapstore-client">thuenen/geonode-mapstore-client</a>
                  |                  |
                  |                  | usergroup/datapackage_tabular-data
                  |                  v
            <a href="https://github.com/GeoNodeUserGroup-DE/geonode-mapstore-client">usergroup/geonode-mapstore-client</a>


                  <a href="https://github.com/geosolutions-it/MapStore2">geosolutions/MapStore2</a>
                              ^
                              | upstream/2024.02.xx
                              |
                   <a href="https://github.com/Thuenen-GeoNode-Development/MapStore2">thuenen/MapStore2</a>
                              
</pre>

## Update Workflow/Merge with Upstream

This description targets stable `4.4.x` to be updated.


### Update geonode-mapstore-client

This is a two way merge:

- `geonode/geonode-mapstore-client` on branch `upstream/4.4.x`
- `usergroup/geonode-mapstore-client` on branch `usergroup/datapackage_tabular-data`

Make sure that all feature development is in sync with targeted upstream branch/version before merge.
For example, the `usergroup/datapackage_tabular-data` branches are in sync with `upstream/4.4.x` for both upstream repositories `geonode/geonode` and `geonode/geonode-mapstore-client`.

> :bulb: Note:
>
> Before merging and testing any changes made to `geonode-mapstore-client` the `MapStore2` submodule must be aligned with upstream first.
> The tracking branches are configured in `.gitmodules` and can be updated with `git submodule update --remote`.

As `geonode-mapstore-client` versions all compiled JavaScript artifacts.
These can be ignored during merge -- `git reset`, `git clean`, and `git restore` are helpful tools here.

Once pushed to remote, GitHub workflow will build the JavaScript artifacts and will create a pull request which can be merged.
After merging the pull request, the `thuenen_atlas` will include latest client build after updating its submodule.


### Update GeoNode

This is a two way merge:

- `geonode/geonode` on branch `upstream/4.4.x`
- `usergroup/geonode` on branch `usergroup/datapackage_tabular-data`



### Update thuenen_atlas

After updating all subcomponents, make sure to update all submodules:

- `geonode-mapstore-client`
- `externalapplications`

After that, update `thuenen_atlas` be merging from `usergroup/geonode-docker-blueprint`.


## Miscellaneous

Here is a somewhat reduced overview of the repository relationships of `thuenen_atlas`:

![Repository Overview](./img/Thünen%20Atlas%20Repository%20Overview.png)