from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from backend.users.choices import UserType
from backend.users.factories import UserFactory
from backend.users.models import User


class CodeChumUserAPIClient(APIClient):
    """Custom APIClient for CodeChum Users

    Injects necessary authentication details to simulate a real request from a client.

    NOTE:
    This Client class creates a minimal `User` instance that only includes the `username` and `password` which means
    that it does not have any related fields that may be included like `University` or `Program`.
    """

    user_type = None

    def __init__(self, user_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user_type:
            self.user_type = user_type

        if self.user_type:
            user = User.objects.create_user(
                username=UserFactory.username(),
                password="generic123",
                user_type=self.user_type,
            )
            token = RefreshToken.for_user(user)

            self.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
            self.force_authenticate(user=user)


class StudentAPIClient(CodeChumUserAPIClient):
    """Student API Client"""

    user_type = UserType.STUDENT


class TeacherAPIClient(CodeChumUserAPIClient):
    """Teacher API Client"""

    user_type = UserType.TEACER


class AdminAPIClient(CodeChumUserAPIClient):
    """Admin API Client"""

    user_type = UserType.ADMIN


class ManagerAPIClient(CodeChumUserAPIClient):
    """Manager API Client"""

    user_type = UserType.MANAGER


class DeanAPIClient(CodeChumUserAPIClient):
    """Dean API Client"""

    user_type = UserType.DEAN
