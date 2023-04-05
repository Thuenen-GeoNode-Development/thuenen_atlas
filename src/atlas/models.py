# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from geonode.base.models import ResourceBase

from geonode.layers.models import Dataset
from geonode.documents.models import Document
from geonode.maps.models import Map
from geonode.geoapps.models import GeoApp
from geonode.groups.models import GroupProfile


# HELPER CLASS
class CustomApplication(models.Model):
    """
    A not by GeoNode or Mapstore created application which shall be part of an Atlas.
    Examples would be the bwi.info application or other external applications
    """

    title = models.CharField(default="A short title", max_length=128, unique=True)
    info = models.TextField(default="some additional information displayed for this custom app")
    url = models.URLField(blank=False)
    thumbnail = models.ImageField(upload_to='atlas/customAppThumbs/%Y/%m', null=True, blank=True,
                                  verbose_name="thumbnail for the app")

    def __str__(self):
        return self.title


# Main Class
class Atlas(models.Model):
    """
    A collection of GeoNode resources (datasets, documents and maps) with additional information like a primer jumbotron
    and multi-media containers as HTML fields.
    """
    group = models.ManyToManyField(GroupProfile, related_name='group_collections', null=True, blank=True)

    # each of those should only contain the appropriate resource type
    #maps = models.ManyToManyField(Map, related_name='map_collections', null=True, blank=True)
    #geoApps = models.ManyToManyField(GeoApp, related_name='geoapp_collections', null=True, blank=True)
    #datasets = models.ManyToManyField(Dataset, related_name='dataset_collections', null=True, blank=True)
    #documents = models.ManyToManyField(Document, related_name='document_collections', null=True, blank=True)
    resource = models.ManyToManyField(ResourceBase, related_name='resource_collections', null=True, blank=True)

    #customApps = models.ManyToManyField(CustomApplication, related_name='customApp_collections', null=True, blank=True,
    #                                    through='AtlasCustomAppListing')

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    # displayed as hero / jumbotron block
    # ! referenced as safe ! HTML is possible
    primer = models.TextField(default="primer")

    jumbotronBackgroundImage = models.ImageField(upload_to='atlas/backgroundImage/%Y/%m', null=True, blank=True,
                                                 verbose_name="Atlas jumbotron background image")

    thumbnail = models.ImageField(upload_to='atlas/thumbs/%Y/%m', null=True, blank=True,
                                  verbose_name="Atlas thumbnail")

    jumbotronBackgroundMovie = models.FileField(upload_to='atlas/mov/%Y/%m', null=True, blank=True,
                                                verbose_name="Atlas jumbotron background movie")

    # should contain bootstrapped html as content block
    # ! referenced as safe ! HTML is possible
    content = models.TextField(default="content")

    def __str__(self):
        return self.name


class AtlasCustomAppListing(models.Model):
    atlas = models.ForeignKey(Atlas, on_delete=models.CASCADE)
    customApp = models.ForeignKey(CustomApplication, on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.atlas.name} : {self.customApp.title} : {self.order}"
