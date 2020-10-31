from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from backend.users.factories import UserFactory

from .models import Task


faker = Faker()


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    name = faker.word
    user = SubFactory(UserFactory)
