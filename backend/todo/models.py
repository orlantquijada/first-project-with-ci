from django.conf import settings
from django.db import models

from backend.generics.models import ArchivableAndSoftDeletionModelMixin


class Task(ArchivableAndSoftDeletionModelMixin):
    name = models.CharField(max_length=100)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )

    def __str__(self):
        return f"{self.id} / {self.name}"  # pylint: disable=no-member
