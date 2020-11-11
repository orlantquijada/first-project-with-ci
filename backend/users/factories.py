from factory import PostGenerationMethodCall
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


class UserFactory(DjangoModelFactory):
    @classmethod
    def _user_type(cls):
        return faker.random_element(choices.UserType.values)

    class Meta:
        model = models.User
        django_get_or_create = ["username"]

    username = faker.unique.user_name
    password = PostGenerationMethodCall("set_password", "generic123")

    first_name = faker.first_name
    last_name = faker.last_name

    university = SubFactory(UniversityFactory)
    user_type = _user_type
