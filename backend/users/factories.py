from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from . import choices
from . import models


faker = Faker()


class UniversityFactory(DjangoModelFactory):
    class Meta:
        model = models.University
        django_get_or_create = ["name"]

    name = faker.unique.company


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ["username"]

    username = faker.unique.user_name
    password = faker.password

    first_name = faker.first_name
    last_name = faker.last_name

    university = SubFactory(UniversityFactory)
    user_type = faker.random_element(choices.UserType.values)


class AdminUserFactory(BaseUserFactory):
    user_type = choices.UserType.ADMIN


class StudentFactory(BaseUserFactory):
    user_type = choices.UserType.STUDENT


class TeacherFactory(BaseUserFactory):
    user_type = choices.UserType.TEACER


class ManagerFactory(BaseUserFactory):
    user_type = choices.UserType.MANAGER
