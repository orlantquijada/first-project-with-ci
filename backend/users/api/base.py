from rest_framework import serializers

from .. import models


class UniversityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.University
        fields = ["id", "name"]
