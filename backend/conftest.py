import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .factories import UserFactory


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def api_client() -> APIClient:
    """Create api client."""
    return APIClient()


@pytest.fixture(scope='function')
def user_authenticated(api_client: APIClient, user: User):
    """Fixture authenticates current user to API."""
    api_client.force_authenticate(user=user)
