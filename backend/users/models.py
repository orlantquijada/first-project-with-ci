from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from backend.generics.models import ArchivableAndSoftDeletionModelMixin
from backend.generics.models import SoftDeletionModelMixin

from . import choices
from . import managers


class University(ArchivableAndSoftDeletionModelMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin, SoftDeletionModelMixin):
    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    user_type = models.CharField(
        max_length=1, choices=choices.UserType.choices, default=choices.UserType.STUDENT
    )

    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        related_name="users",
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = managers.UserManager()

    def __str__(self):
        return f"{self.id} / {self.first_name}"  # pylint: disable=no-member

    def is_student(self):
        return self.user_type == choices.UserType.STUDENT

    def is_teacher(self):
        return self.user_type == choices.UserType.TEACHER

    def is_manager(self):
        return self.user_type == choices.UserType.MANAGER

    def is_admin(self):
        return self.user_type == choices.UserType.ADMIN

    def is_dean(self):
        return self.user_type == choices.UserType.DEAN
