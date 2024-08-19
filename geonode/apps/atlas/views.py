# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _
from django.http import HttpResponse

from .models import Atlas, AtlasCustomAppListing


class AtlasDetail(DetailView):
    model = Atlas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.public or self.request.user.is_authenticated:
            context["customApps"] = AtlasCustomAppListing.objects.filter(
                atlas=context["atlas"]
            )
            return context
        else:
            return HttpResponse(_("Not allowed"), status=403)


class AtlasList(ListView):
    model = Atlas


class AtlasView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Atlas.objects.all()
        return context
