from django.contrib.auth import get_user_model
import pytest

@pytest.mark.django_db
class TestSignUpAPI:
  def test_signup_with_valid_data(self, api_client, user_payload_factory):
    response = api_client.post("/api/auth/register/", data=user_payload_factory(), format="json")    
    assert response.status_code == 201
    assert "password" not in response.json()['user']

    user_id = response.json()['user']['id']
    
    user = get_user_model().objects.filter(id=user_id).first()
    assert user is not None
    assert user.id == user_id
    assert user.email == response.json()['user']['email']
    assert user.username == response.json()['user']['username']
    