from rest_framework import status
from rest_framework.test import APITestCase

from . import factories
from . import models


class UniversityTests(APITestCase):
    def setUp(self):
        self.url = "/api/v1/universities/"
        self.factory = factories.UniversityFactory

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
