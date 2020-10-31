from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=["GET"])
    def check(self, request):
        return Response(f"{request.user.user_type}")
