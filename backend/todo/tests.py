import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class TaskViewSetTest(APITestCase):
    def test_task_list(self):
        url = reverse("task-list")
        response = self.client.get(url, format="json")

        print(datetime.datetime.now())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(timezone.is_aware(datetime.datetime.now()), False)
        self.assertEqual(timezone.is_aware(timezone.now()), True)
