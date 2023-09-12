# Thuenen Atlas

The Atlas app is a contrib module for GeoNode.
The app is compatible with GeoNode v4 and GeoNode MapStore Client v4.

The app adds overridden `geonode_base.html` templates which provides some basic information to a visitor.
The templates gives inforamtion about curated content called an `Atlas`.
An `Atlas` is a collection of other GeoNode resources and is stored in the database as a resource type along with some accompanying models. 
An `Atlas` instance can be curated in the Django Admin.

## Installation and Configuration

To activate the Atlas app, add the following to the `settings.py`:

```py
INSTALLED_APPS += ( 'atlas', )
```

Create database migrations and apply them via:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Add a Filter Menu

In case you want to manually add a menu entry use the GeoNode admin.
First create a `Menu` _Atlases_ which you put under placeholder `TOPBAR_MENU_LEFT`. 
After that, create a `MenuItem` to create a `MenuItem` _Atlases_ and select the `Menu` you created.
To filter all external applications add the URL `/atlanten`.