import logging
import urllib.parse
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.db.models import QuerySet
from django import forms
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from geonode.base.models import ResourceBase

from .models import RemoteGeoNodeInstance, RemotePushSession, RemotePushJob
from .tasks import remote_push_session_task

logger = logging.getLogger("geonode.push_to_remote")


def reverse_model_list_link(model, *args, **kwargs) -> str:
    return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist", *args, **kwargs)


def reverse_model_link(model, *args, **kwargs) -> str:
    return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_change", *args, **kwargs)

def reverse_model_link_html(model, label=None):
    if not label:
        label = model
    url = reverse_model_link(model, args=(model.pk,))
    return mark_safe(format_html(f'<a href="{url}">{label}</a>'))

class RemoteGeoNodeInstanceForm(forms.ModelForm):
    class Meta:
        model = RemoteGeoNodeInstance
        fields = ["name", "url", "username", "password"]
        widgets = {"password": forms.PasswordInput()}


@admin.register(RemoteGeoNodeInstance)
class RemoteGeoNodeInstanceAdmin(admin.ModelAdmin):
    model = RemoteGeoNodeInstance
    form = RemoteGeoNodeInstanceForm
    list_display = ("name", "url")
    list_display_links = ("name", "url")


class PushForm(forms.Form):
    target_instance = forms.ModelChoiceField(RemoteGeoNodeInstance.objects.all(),
                                             required=True,
                                             label="Target GeoNode Instance")
    force_push = forms.BooleanField(label="Force Push", initial=False, required=False)


@admin.register(RemotePushSession)
class RemotePushSessionAdmin(admin.ModelAdmin):
    model = RemotePushSession
    list_display = ("pk", "remote_link", "started", "updated", "ended", "force", "initiator_link", "status", "progress", "jobs_link")
    #list_display_links = ("pk",)
    list_filter = ("remote", "force", "status")
    readonly_fields = ("remote", "started", "updated", "ended", "details", "force", "initiator", "status", "total_resources_to_process", "resources_done")
    actions = ["abort"]

    @admin.display(description="Progress")
    def progress(self, session: RemotePushSession) -> int:
        done, total = (session.resources_done, session.total_resources_to_process)
        progress = 0 if total == 0 else (done / total) * 100
        return f"{int(progress)}%"

    @admin.display(description="Jobs")
    def jobs_link(self, session: RemotePushSession):
        uri = reverse_model_list_link(RemotePushJob)
        return mark_safe(
            format_html(
                f'<a class="button grp-button" href="{uri}?session__id__exact={session.pk}">({session.total_resources_to_process}) Go</a>'
            )
        )

    @admin.display(description="Target GeoNode Instance", ordering="remote")
    def remote_link(self, session: RemotePushSession):
        return reverse_model_link_html(session.remote)

    @admin.display(description="Initiator", ordering="initiator")
    def initiator_link(self, session: RemotePushSession):
        return reverse_model_link_html(session.initiator)

    @admin.action(description="Abort")
    def abort(self, request: HttpRequest, queryset: QuerySet):
        for session in queryset:
            session.abort()
        self.message_user(request, "Push session have been aborted")

    def delete_queryset(self, request, queryset):
        for session in queryset:
            session.delete()
        self.message_user(request, "Push sessions have been deleted")


@admin.register(RemotePushJob)
class RemotePushJobAdmin(admin.ModelAdmin):
    model = RemotePushJob
    list_display = ("pk", "session_link", "resource_link", "remote_link", "initiator_link", "status", "started", "updated", "ended", "remote_url")
    list_filter = ("session", "resource", "status")
    readonly_fields = ("resource", "status", "session", "started", "updated", "ended", "details")
    actions = ["abort"]
    
    @admin.display(description="Resource", ordering="resource")
    def resource_link(self, job: RemotePushJob):
        resource = ResourceBase.objects.polymorphic_queryset().get(pk=job.resource.pk)
        return reverse_model_link_html(resource)

    @admin.display(description="Session", ordering="session")
    def session_link(self, job: RemotePushJob):
        url = reverse_model_link(job.session, args=(job.session.pk,))
        return mark_safe(format_html(f'<a href="{url}">{job.session}</a>'))

    @admin.display(description="Pushed remote resource")
    def remote_url(self, job: RemotePushJob):
        if job.status == RemotePushJob.Status.SUCCESS:
            url = urllib.parse.urljoin(job.session.remote.url, f"catalogue/uuid/{job.resource.uuid}")
            return mark_safe(format_html(f'<a href="{url}">Pushed remote resource</a>'))

    @admin.display(description="Target GeoNode Instance", ordering="session.remote")
    def remote_link(self, job: RemotePushJob):
        return reverse_model_link_html(job.session.remote)

    @admin.display(description="Initiator", ordering="session.initiator")
    def initiator_link(self, job: RemotePushJob):
        return reverse_model_link_html(job.session.initiator)

    @admin.action(description="Abort")
    def abort(self, request: HttpRequest, queryset: QuerySet):
        for job in queryset:
            job.abort()
        self.message_user(request, "Push jobs have been aborted")
    
    def delete_queryset(self, request, queryset):
        for job in queryset:
            job.delete()
        self.message_user(request, "Push jobs have been deleted")


@admin.action(description="Push to remote instance")
def push_to_remote(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    if "apply" in request.POST:
        form = PushForm(request.POST)
        if form.is_valid():
            session = RemotePushSession.create(remote=form.cleaned_data["target_instance"],
                                               force=form.cleaned_data["force_push"],
                                               initiator=request.user,
                                               queryset=queryset)
            remote_push_session_task.delay(session.pk)
            uri = reverse_model_list_link(RemotePushJob)
        return HttpResponseRedirect(f"{uri}?session__id__exact={session.pk}")
    elif "cancel" in request.POST:
        return HttpResponseRedirect(request.get_full_path())
    else:
        form = PushForm()
        return render(request, "admin/push_to_remote.html",
                      context={"resources": queryset, "form": form})


try:
    from geonode.layers.admin import DatasetAdmin
    DatasetAdmin.actions += [push_to_remote]
except:
    pass

try:
    from geonode.documents.admin import DocumentAdmin
    DocumentAdmin.actions += [push_to_remote]
except:
    pass
