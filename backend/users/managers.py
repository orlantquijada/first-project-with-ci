from django.contrib.auth.models import BaseUserManager

from backend.generics.models import SoftDeletionManager


class UserManager(BaseUserManager, SoftDeletionManager):
    def create_superuser(self, username, password=None, **other_fields):
        user = self.create_user(username, password, **other_fields)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user

    def create_user(self, username, password, **other_fields):
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()

        return user
