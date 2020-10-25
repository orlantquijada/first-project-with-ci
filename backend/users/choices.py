from django.db import models


class UserType(models.TextChoices):
    STUDENT = ("S", "Student")
    TEACER = ("T", "Teacher")
    ADMIN = ("A", "Admin")
    MANAGER = ("M", "Manager")
    DEAN = ("D", "Dean")
