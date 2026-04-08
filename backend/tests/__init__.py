import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        full_name='Test User'
    )

@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user(self, api_client):
        response = api_client.post('/api/v1/auth/register/', {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'full_name': 'New User',
        })
        assert response.status_code == 201

@pytest.mark.django_db
class TestUserLogin:
    def test_login_user(self, api_client, user):
        response = api_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123',
        })
        assert response.status_code == 200
        assert 'tokens' in response.json()
