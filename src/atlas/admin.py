# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Atlas, CustomApplication, AtlasCustomAppListing


class AtlasAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('resource',)


admin.site.register(Atlas, AtlasAdmin)
admin.site.register(CustomApplication)
admin.site.register(AtlasCustomAppListing)
