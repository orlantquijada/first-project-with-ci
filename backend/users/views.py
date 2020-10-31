from rest_framework import mixins
from rest_framework import viewsets

from . import models
from . import serializers


class UniversityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.University.objects.all()
    serializer_class = serializers.UniversityModelSerializer
