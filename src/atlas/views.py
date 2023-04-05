# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Atlas, AtlasCustomAppListing
from django.views.generic import DetailView, ListView


# Create your views here.

class AtlasDetail(DetailView):
    model = Atlas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customApps'] = AtlasCustomAppListing.objects.filter(atlas=context['atlas'])
        return context

class AtlasList(ListView):
    model = Atlas

from django.views.generic.base import TemplateView
class AtlasView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Atlas.objects.all()
        return context
    
class AtlasDetailView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Atlas.objects.all()
        return context