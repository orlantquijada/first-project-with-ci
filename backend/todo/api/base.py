from rest_framework import serializers

from backend.todo import models


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["id", "name", "user"]
