from rest_framework import mixins
from rest_framework import viewsets

from . import models
from . import serializers


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskModelSerializer
