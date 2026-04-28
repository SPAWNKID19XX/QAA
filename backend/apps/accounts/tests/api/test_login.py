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
        assert isinstance(response_data["access"], str)
        assert len(response_data["access"]) > 0
        assert isinstance(response_data["refresh"], str)
        assert len(response_data["refresh"]) > 0
        assert "refresh" in response_data
        assert "user" in response_data

        
        user_data = response_data['user']
        assert len(user_data) == 3
        assert user_data['id'] == user.id
        assert user_data['username'] == user.username
        assert user_data['role'] == user.role
        assert "password" not in user_data

    def test_login_additional_fields_ignored(self, api_client, user_factory):
        user = user_factory()

        response = api_client.post("/api/auth/login/", data={
            "username": user.username,
            "password": "testpass",
            "extra_field": "extra_value"
        }, format="json")
        assert response.status_code == 200

        response_data = response.json()

        assert len(response_data) == 3
        assert "access" in response_data
        assert "refresh" in response_data
        assert "user" in response_data
        assert "extra_field" not in response_data

    def test_login_with_spaces_before_after_username_successed(self, api_client, user_factory):
        user = user_factory()

        response = api_client.post("/api/auth/login/", data={
            "username": f"  {user.username}  ",
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

    def test_login_CamelCase_username_successed(self, api_client, user_factory):
        user = user_factory(username="TestUser")

        response = api_client.post("/api/auth/login/", data={
            "username": "TestUser",
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

    def test_login_CamelCase_password_successed(self, api_client, user_factory):
        user = user_factory(password="TestPass")

        response = api_client.post("/api/auth/login/", data={
            "username": user.username,
            "password": "TestPass"
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

    def test_login_with_spaces_before_after_password_successed(self, api_client, user_factory):
        user = user_factory()

        response = api_client.post("/api/auth/login/", data={
            "username": f"{user.username}",
            "password": "  testpass  "
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

    def test_login_with_empty_body_fails(self, api_client, user_factory):
        response = api_client.post("/api/auth/login/", data={}, format="json")
        assert response.status_code == 400
        assert "username" in response.json()
        assert "password" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_with_blank_username_fails(self, api_client):
        response = api_client.post("/api/auth/login/", data={
            "username": "",
            "password": "testpass"
        }, format="json")
        assert response.status_code == 400
        assert "username" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_with_blank_password_fails(self, api_client):
        response = api_client.post("/api/auth/login/", data={
            "username": "test_username",
            "password": ""
        }, format="json")
        assert response.status_code == 400
        assert "password" in response.json() 
        assert "access" not in response.json()
        assert "refresh" not in response.json() 

    def test_login_with_nonexistent_user_fails(self, api_client):
        response = api_client.post("/api/auth/login/", data={
            "username": "nonexistent_user",
            "password": "testpass"
        }, format="json")
        assert response.status_code == 401
        assert "detail" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_with_spaces_username_field_fails(self, api_client, user_factory):
        response = api_client.post("/api/auth/login/", data={
            "username": " ",
            "password": "testpass"
        }, format="json")

        assert response.status_code == 400
        assert "username" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_with_spaces_password_field_fails(self, api_client, user_factory):
        response = api_client.post("/api/auth/login/", data={
            "username": "test_username",
            "password": " "
        }, format="json")
        assert response.status_code == 400
        assert "password" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_invalid_credentials_fails(self, api_client):
        
        response = api_client.post("/api/auth/login/", data={
            "username": "wrong_username",
            "password": "wrong_password"
        }, format="json")

        assert response.status_code == 401
        assert "detail" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_missing_username_fails(self, api_client):
        response = api_client.post("/api/auth/login/", data={
            "password": "testpass"
        }, format="json")
        assert response.status_code == 400
        assert "username" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_missing_password_fails(self, api_client): 
        response = api_client.post("/api/auth/login/", data={
            "username": "test_username"
        }, format="json")
        assert response.status_code == 400
        assert "password" in response.json()  
        assert "access" not in response.json()
        assert "refresh" not in response.json()

    def test_login_with_is_inactive_user_fails(self, api_client, user_factory):
        
        user = user_factory(is_active=False)

        response = api_client.post("/api/auth/login/", data={
            "username": user.username,
            "password": "testpass"
        }, format="json")
        assert response.status_code == 401
        assert "detail" in response.json()
        assert "access" not in response.json()
        assert "refresh" not in response.json()


    @pytest.mark.parametrize("method", ["get", "delete", "patch", "put"])
    def test_login_wrong_methods_return_405(self, api_client, method):                              
      response = getattr(api_client, method)("/api/auth/login/")                                  
      assert response.status_code == 405
      assert "detail" in response.json()
      assert "access" not in response.json()
      assert "refresh" not in response.json()       

    def test_login_head_405(self, api_client):
        response = api_client.head("/api/auth/login/")
        assert response.status_code == 405
