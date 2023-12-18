from dynamic_rest.serializers import DynamicModelSerializer

from ..models import RemotePushJob


class RemotePushJob(DynamicModelSerializer):
    class Meta:
        model = RemotePushJob
        name = "remote-push-job"
