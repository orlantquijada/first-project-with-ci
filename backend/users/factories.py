from factory import PostGenerationMethodCall
from factory import SubFactory
from factory import Faker as factory_faker
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import BaseProvider

from . import choices
from . import models


faker = Faker()


class UniversityFactory(DjangoModelFactory):
    class Meta:
        model = models.University
        django_get_or_create = ["name"]

    name = faker.unique.company


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ["username"]

    username = faker.unique.user_name
    password = PostGenerationMethodCall("set_password", "generic123")

    first_name = faker.first_name
    last_name = faker.last_name

    university = SubFactory(UniversityFactory)
    user_type = _user_type
