from django.contrib.auth import get_user_model
import pytest

@pytest.mark.django_db
class TestSignUpAPI:
  def test_signup_with_valid_data(self, api_client, user_payload_factory):

    response = api_client.post("/api/auth/register/", data=user_payload_factory(), format="json")    
    response_data = response.json()
    data_user = response.json()['user']
    
    assert response.status_code == 201
    assert "password" not in data_user
    assert "access" in response_data
    assert "refresh" in response_data

    user = get_user_model().objects.filter(id=data_user['id']).first()
    
    assert user is not None
    assert user.id == data_user['id']
    assert user.email == data_user['email']
    assert user.username == data_user['username']
    assert user.is_active
    assert not user.is_staff
    assert user.date_joined is not None

  def test_signup_with_spaces_username(self, api_client, user_payload_factory):
    payload_data = user_payload_factory(username="      ")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(username=payload_data['username']).first()

    assert response.status_code == 400
    assert "username" in response_data
    assert user is None

  def test_signup_without_role_defaults_to_user(self, api_client, user_payload_factory):
    payload_data = user_payload_factory()

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()
    data_user = response_data['user']

    assert response.status_code == 201
    assert data_user['role'] == "user"

    user = get_user_model().objects.filter(id=data_user['id']).first()

    assert user is not None
    assert user.role == "user"

  def test_signup_without_email_data_succeeds(self, api_client, user_payload_factory):
    payload_data = user_payload_factory()
    payload_data.pop("email")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()
    data_user = response_data['user']

    assert response.status_code == 201

    user = get_user_model().objects.filter(id=data_user['id']).first()

    assert user is not None
    assert user.email == ""

  def test_signup_password_is_hashed(self, api_client, user_payload_factory):
    payload_data = user_payload_factory()
    password = payload_data['password']

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()
    data_user = response_data['user']

    assert response.status_code == 201

    user = get_user_model().objects.filter(id=data_user['id']).first()

    assert user is not None
    assert user.password != password
    assert user.check_password(password)
  
  def test_signup_with_duplicate_email(self, api_client, user_payload_factory):
    email=user_payload_factory()['email']
    response = api_client.post("/api/auth/register/", data=user_payload_factory(email=email), format="json")
    response2 = api_client.post("/api/auth/register/", data=user_payload_factory(email=email), format="json")

    user_counter = get_user_model().objects.filter(email=email).count()

    assert response.status_code == 201
    assert response2.status_code == 201
    assert user_counter == 2
  
  def test_signup_with_duplicate_userdata_fails(self, api_client, user_payload_factory):

    payload_data = user_payload_factory()
    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response2 = api_client.post("/api/auth/register/", data=payload_data, format="json")

    response2_data = response2.json()

    user_counter = get_user_model().objects.filter(username=payload_data['username']).count()

    assert response.status_code == 201
    assert response2.status_code == 400
    assert "username" in response2_data
    assert user_counter == 1

  def test_signup_with_invalid_email_fails(self, api_client, user_payload_factory):
    
    payload_data = user_payload_factory(email="invalid_email")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(username=payload_data['username']).first()

    assert response.status_code == 400
    assert "email" in response_data
    assert user is None

  def test_signup_with_empty_username_fails(self, api_client, user_payload_factory):
    payload_data = user_payload_factory(username="")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(username=payload_data['username']).first()

    assert response.status_code == 400
    assert "username" in response_data
    assert user is None

  def test_signup_without_username_fails(self, api_client, user_payload_factory):
    payload_data = user_payload_factory()
    payload_data.pop("username")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(email=payload_data['email']).first()

    assert response.status_code == 400
    assert "username" in response_data
    assert user is None

  def test_signup_with_weak_password_fails(self, api_client, user_payload_factory):
    
    payload_data = user_payload_factory(password="123")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(username=payload_data['username']).first()

    assert response.status_code == 400
    assert "password" in response_data
    assert user is None

  def test_signup_without_password_fails(self, api_client, user_payload_factory):
    payload_data = user_payload_factory()
    payload_data.pop("password")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()

    user = get_user_model().objects.filter(username=payload_data['username']).first()

    assert response.status_code == 400
    assert "password" in response_data
    assert user is None

  def test_signup_without_required_fields_fails(self, api_client, user_payload_factory):

    payload_data = user_payload_factory()
    username = payload_data['username']
    payload_data.pop("password")
    payload_data.pop("username")

    response = api_client.post("/api/auth/register/", data=payload_data, format="json")
    response_data = response.json()


    user = get_user_model().objects.filter(username=username).first()

    assert response.status_code == 400
    assert "password" in response_data 
    assert "username" in response_data
    assert user is None

  @pytest.mark.parametrize('method',["get","put","delete","patch"])
  def test_dangerous_http_methods_signup_endpoint_fails(self,method ,api_client, user_payload_factory):
    payload_data = user_payload_factory()
    response = getattr(api_client, method)("/api/auth/register/", data=payload_data, format="json")
    assert response.status_code == 405