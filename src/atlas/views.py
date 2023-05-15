# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from .models import Atlas, AtlasCustomAppListing


class AtlasDetail(DetailView):
    model = Atlas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.object.public or self.request.user.is_authenticated):
            context["customApps"] = AtlasCustomAppListing.objects.filter(
                atlas=context["atlas"]
            )
        else:
            return HttpResponse(_("Not allowed"), status=403)
        return context


class AtlasList(ListView):
    model = Atlas


class AtlasView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Atlas.objects.all()
        return context
