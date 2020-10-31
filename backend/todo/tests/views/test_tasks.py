from rest_framework import status
from rest_framework.test import APITestCase

from backend.generics.clients import CodeChumUserAPIClient
from backend.generics.clients import TeacherAPIClient
from backend.todo.api.base import TaskModelSerializer
from backend.todo.factories import TaskFactory
from backend.todo.models import Task
from backend.users.choices import UserType
from backend.users.factories import UserFactory


class TaskViewSetTest(APITestCase):
    client_class = TeacherAPIClient

    url = "/api/v1/tasks/"
    factory = TaskFactory
    model = Task
    serializer = TaskModelSerializer

    def test_create_task(self):
        user = UserFactory()
        data = {"name": self.factory.name(), "user": user.id}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tasks(self):
        number_of_tasks_to_create = 3
        self.factory.create_batch(number_of_tasks_to_create)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_type_check(self):
        student_client = CodeChumUserAPIClient(user_type=UserType.STUDENT)
        teacher_client = CodeChumUserAPIClient(user_type=UserType.TEACER)
        admin_client = CodeChumUserAPIClient(user_type=UserType.ADMIN)
        manager_client = CodeChumUserAPIClient(user_type=UserType.MANAGER)
        dean_client = CodeChumUserAPIClient(user_type=UserType.DEAN)

        url = f"{self.url}check/"

        student_response = student_client.get(url)
        teacher_response = teacher_client.get(url)
        admin_response = admin_client.get(url)
        manager_response = manager_client.get(url)
        dean_response = dean_client.get(url)

        self.assertEqual(student_response.status_code, status.HTTP_200_OK)

        self.assertEqual(student_response.data, UserType.STUDENT)
        self.assertEqual(teacher_response.data, UserType.TEACER)
        self.assertEqual(admin_response.data, UserType.ADMIN)
        self.assertEqual(manager_response.data, UserType.MANAGER)
        self.assertEqual(dean_response.data, UserType.DEAN)
