from rest_framework import status
from rest_framework.test import APITestCase

from backend.generics.clients import StudentAPIClient
from backend.users.api.base import UniversityModelSerializer
from backend.users.choices import UserType
from backend.users.factories import UniversityFactory, UserFactory
from backend.users.models import University


class UniversityTests(APITestCase):
    client_class = StudentAPIClient

    base_url = "/api/v1/universities/"
    factory = UniversityFactory
    serializer = UniversityModelSerializer
    model = University

    def test_create_university(self):
        data = {"name": self.factory.name()}
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_universities(self):
        number_of_universities_to_create = 5
        universities = self.factory.create_batch(number_of_universities_to_create)
        serializer = self.serializer(universities, many=True)

        response = self.client.get(self.base_url)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_university(self):
        university = self.factory()
        serializer = self.serializer(university)

        response = self.client.get(f"{self.base_url}{university.id}/")

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_university(self):
        university = self.factory()

        response = self.client.delete(f"{self.base_url}{university.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_type(self):
        response = self.client.get(f"{self.base_url}test_user/")

        print(response.data)

        # assert actual == expected
        self.assertEqual(response.data, UserType.STUDENT)
