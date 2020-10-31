from rest_framework import status
from rest_framework.test import APITestCase

from backend.generics.clients import StudentAPIClient
from backend.users.api.base import UniversityModelSerializer
from backend.users.factories import UniversityFactory
from backend.users.models import University


class UniversityTests(APITestCase):
    client_class = StudentAPIClient

    url = "/api/v1/universities/"
    factory = UniversityFactory

    def test_create_university(self):
        data = {"name": self.factory.name()}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_universities(self):
        number_of_universities_to_create = 5
        self.factory.create_batch(number_of_universities_to_create)

        response = self.client.get(self.url)

        self.assertEqual(University.objects.count(), number_of_universities_to_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_university(self):
        university = self.factory()
        serializer = UniversityModelSerializer(university)

        response = self.client.get(f"{self.url}{university.id}/")

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
