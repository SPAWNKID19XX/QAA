import pytest
from django.contrib.auth import get_user_model



@pytest.mark.django_db
class TestLogin:
    def test_login_valid_credentials_successed(self, api_client, user_factory):
        user = user_factory()

        response = api_client.post("/api/auth/login/", data={
            "username": user.username,
            "password": "testpass"
        }, format="json")
        assert response.status_code == 200

        response_data = response.json()
        assert "access" in response_data
        assert "refresh" in response_data
        assert "user" in response_data

        
        user_data = response_data['user']
        assert len(user_data) == 3
        assert user_data['id'] == user.id
        assert user_data['username'] == user.username
        assert user_data['role'] == user.role
        assert "password" not in user_data
        
