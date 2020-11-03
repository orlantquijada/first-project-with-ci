from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=["GET"])
    def test_user(self, request):
        return Response(f"{self.request.user.user_type}")
