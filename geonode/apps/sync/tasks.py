

from .models import RemotePushJob, RemotePushSession
from .serializers import create_serializer
from celery import group
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from geonode.celery_app import app
from geonode.storage.manager import StorageManager
from sync.models import RemotePushJob
from sync.serializers import create_serializer
import io
import json
import logging
import requests
import typing
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

logger = logging.getLogger(__name__)

QUEUE = "geonode"


@app.task(queue=QUEUE)
def scheduler():
    pass


@app.task(queue=QUEUE)
def remote_push_session_task(session_id: int):
    session = RemotePushSession.objects.get(pk=session_id)
    if session.status in [
        RemotePushSession.Status.ABORTING,
        RemotePushSession.Status.ABORTED,
    ]:
        logger.info(f"skipping session {session} as the session was aborted")
    if session.set_running():
        jobs = RemotePushJob.objects.filter(session=session)
        subtasks = group(remote_push_job_task.s(session.pk, job.pk) for job in jobs)
        callback = remote_push_session_task_finalizer.s(session_id=session_id)
        (subtasks | callback).delay()


@app.task(queue=QUEUE)
def remote_push_session_task_finalizer(session_id: int = None) -> RemotePushJob.Status:
    session = RemotePushSession.objects.get(pk=session_id)
    jobs = RemotePushJob.objects.filter(session=session)
    if session.status == RemotePushJob.Status.ABORTING:
        return session.finish(RemotePushJob.Status.ABORTED)
    else:
        return session.finish(get_finished_session_status(jobs))


def get_finished_session_status(jobs: typing.List[RemotePushJob]):
    success = False
    failure = False
    aborted = False
    for job in jobs:
        if job.status == RemotePushJob.Status.SUCCESS:
            success = True
        elif job.status == RemotePushJob.Status.FAILURE:
            failure = True
        elif job.status == RemotePushJob.Status.ABORTED:
            aborted = True
    if failure and success:
        return RemotePushSession.Status.PARTIAL_FAILURE
    elif success:
        return RemotePushSession.Status.SUCCESS
    elif failure:
        return RemotePushSession.Status.FAILURE
    elif aborted:
        return RemotePushSession.Status.ABORTED
    else:
        return RemotePushSession.Status.FAILURE


@app.task(queue=QUEUE)
def remote_push_job_task(session_id: int, job_id: int) -> RemotePushJob.Status:
    session = RemotePushSession.objects.get(pk=session_id)
    job = RemotePushJob.objects.get(pk=job_id)
    if session.status in [
        RemotePushSession.Status.ABORTING,
        RemotePushSession.Status.ABORTED,
    ]:
        logger.info(f"skipping Job {job} as the session was aborted")
    if job.set_running():
        try:
            push_resource(session, job)
            logger.info(f"Job {job} finished successfully")
            return job.finish(RemotePushJob.Status.SUCCESS)
        except Exception as error:
            logger.warning(f"Job {job} failed: {error}")
            return job.finish(RemotePushJob.Status.FAILURE, repr(error))
    else:
        return job.status


def resource_to_json(resource):
    serializer = create_serializer(resource._meta.model)()
    representation = serializer.to_representation(resource)
    return json.dumps(representation, cls=DjangoJSONEncoder)

def push_resource(session: RemotePushSession, job: RemotePushJob):
    logger.info(f"pushing resource {job.resource}")
    # get the actual resource
    resource = job.resource.polymorphic_ctype.get_object_for_this_type(pk=job.resource.pk)
    storageManager = StorageManager()

    files = files = {
        BASE_FILE: (
            "resource.json",
            io.StringIO(resource_to_json(resource)),
            "application/json",
        ),
    }

    if resource.files:
        for idx, path in enumerate(resource.files):
            files[f"files[{idx}]"] = (path, storageManager.open(path))

    # add the thumbnail to the request, this is available
    if resource.thumbnail_path:
        files[THUMBNAIL_FILE] = (
            resource.thumbnail_path,
            storageManager.open(resource.thumbnail_path),
        )

    datasetContentType = ContentType.objects.get(app_label="layers", model="dataset")
    # add the actual dataset to the request
    if resource.polymorphic_ctype == datasetContentType:
        # either as GeoJSON
        if resource.subtype == "vector":
            url = resource.link_set.get(link_type="data", mime="json").url
            url = fix_geoserver_url(url)
            response = requests.get(url)
            response.raise_for_status()
            files["data"] = ("data.json",response.content)
        # or as GeoTIFF
        elif resource.subtype == "raster":
            url = resource.link_set.get(link_type="data", mime="image/tiff").url
            url = fix_geoserver_url(url)
            response = requests.get(url)
            response.raise_for_status()
            files["data"] = ("data.tiff", response.content)

        files[STYLE_FILE] = ("style.sld", resource.default_style.sld_body)

    auth = (session.remote.username, session.remote.password)
    url = f"{session.remote.url}/sync/receive"
    # TODO remove webhook.site
    # url = "https://webhook.site/20feca89-00f7-4d8b-943f-df7f20a6c901"
    data = {"force": session.force, "uuid": resource.uuid}
    url = "https://webhook.site/c31981af-00ab-4110-aa38-e1975551b5a3"
    data = { "force": session.force, "uuid": resource.uuid }
    response = requests.post(url, files=files, auth=auth, data=data)
    response.raise_for_status()


def fix_geoserver_url(url):
    # do an internal geoserver request, else it won't work for localhost setups
    if "localhost" in url:
        if settings.GEOSERVER_PUBLIC_LOCATION in url:
            url = url.replace(settings.GEOSERVER_PUBLIC_LOCATION, settings.GEOSERVER_LOCATION)
        # yeah... I just don't care anymore......
        if "http://localhost:8080/geoserver/" in url:
            url = url.replace("http://localhost:8080/geoserver/", settings.GEOSERVER_LOCATION)
    return url
