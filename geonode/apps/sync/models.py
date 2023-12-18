import logging
from django.db import models
from geonode.base.models import ResourceBase
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import F
from django.utils import timezone

logger = logging.getLogger(__name__)


class RemoteGeoNodeInstance(models.Model):
    name = models.CharField(max_length=256, blank=False)
    url = models.URLField(max_length=1024, blank=False)
    username = models.CharField(max_length=256, blank=False)
    password = models.CharField(max_length=256, blank=False)

    class Meta:
        verbose_name = "Remote GeoNode Instance"

    def __str__(self) -> str:
        return self.name


class RemotePushSession(models.Model):
    class Meta:
        verbose_name = "Remote Push Session"

    class Status(models.TextChoices):
        PENDING = "PENDING", _("pending")
        RUNNING = "RUNNING", _("running")
        SUCCESS = "SUCCESS", _("success")
        FAILURE = "FAILURE", _("failure")
        ABORTING = "ABORTING", _("aborting")
        ABORTED = "ABORTED", _("aborted")
        PARTIAL_FAILURE = "PARTIAL_FAILURE", _("partial failure")

    remote = models.ForeignKey(RemoteGeoNodeInstance, null=False, on_delete=models.CASCADE)
    started = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ended = models.DateTimeField(null=True, blank=True)
    details = models.TextField(blank=True)
    force = models.BooleanField(default=False)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_resources_to_process = models.IntegerField(
        default=0, help_text=_("Number of resources being processed in this session")
    )
    resources_done = models.IntegerField(default=0, help_text=_("Number of resources that have already been processed"))

    def abort(self) -> None:
        if self.status == self.Status.PENDING:
            self.finish(self.Status.ABORTED)
        elif self.status == self.Status.RUNNING:
            self.status = self.Status.ABORTING
        else:
            logger.debug(f"Session {self} is not currently in an state that can be aborted, skipping...")
        self.save()
        for job in RemotePushJob.objects.filter(session=self):
            job.abort()

    def finish(self, status: Status, details="") -> Status:
        self.status = status
        self.details = details
        self.ended = timezone.now()
        self.save()
        return status

    def set_running(self):
        if self.status == self.Status.ABORTING:
            self.finish(self.Status.ABORTED)
        elif self.status == self.Status.PENDING:
            self.status = self.Status.RUNNING
            self.save()
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    def inc_resources_done(self, amount: int = 1):
        RemotePushSession.objects.filter(pk=self.pk).update(resources_done=F("resources_done") + amount)

    @classmethod
    def create(cls, remote: RemoteGeoNodeInstance, force: bool, initiator, queryset):
        session = cls.objects.create(
            remote=remote, force=force, initiator=initiator, total_resources_to_process=queryset.count()
        )
        for resource in queryset:
            session.create_job(resource)
        return session

    def create_job(self, resource: ResourceBase):
        return RemotePushJob.create(resource=resource, session=self)

    def __str__(self) -> str:
        return f"{self.pk}"


class RemotePushJob(models.Model):
    class Meta:
        verbose_name = "Remote Push Job"

    class Status(models.TextChoices):
        PENDING = "PENDING", _("pending")
        RUNNING = "RUNNING", _("running")
        SUCCESS = "SUCCESS", _("success")
        FAILURE = "FAILURE", _("failure")
        ABORTING = "ABORTING", _("aborting")
        ABORTED = "ABORTED", _("aborted")

    resource = models.ForeignKey(ResourceBase, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING, null=False)
    session = models.ForeignKey(RemotePushSession, on_delete=models.CASCADE, null=False)
    started = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ended = models.DateTimeField(null=True, blank=True)
    details = models.TextField(blank=True)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls.objects.create(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)

    def abort(self) -> None:
        if self.status == self.Status.PENDING:
            self.finish(self.Status.ABORTED)
        elif self.status == self.Status.RUNNING:
            self.status = self.Status.ABORTING
        else:
            logger.debug(f"Job {self} is not currently in an state that can be aborted, skipping...")

        self.save()

    def set_running(self):
        if self.status == self.Status.ABORTING:
            self.finish(self.Status.ABORTED)
        elif self.status == self.Status.PENDING:
            self.status = self.Status.RUNNING
            self.save()
            return True
        return False

    def finish(self, status: Status, details="") -> Status:
        self.status = status
        self.details = details
        self.ended = timezone.now()
        self.save()
        self.session.inc_resources_done()
        return status

    def __str__(self) -> str:
        return f"{self.pk}"
