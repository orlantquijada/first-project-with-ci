from rest_framework import status
from rest_framework.test import APITestCase

from backend.generics.clients import StudentAPIClient
from backend.users import factories
from backend.users import models


class UniversityTests(APITestCase):
    client_class = StudentAPIClient

    url = "/api/v1/universities/"
    factory = factories.UniversityFactory

    def test_create_university(self):
        data = {"name": self.factory.name()}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_universities(self):
        number_of_universities_to_create = 5
        self.factory.create_batch(number_of_universities_to_create)

        response = self.client.get(self.url)

        self.assertEqual(
            models.University.objects.count(), number_of_universities_to_create
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)