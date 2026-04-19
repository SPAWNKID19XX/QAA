from django.contrib.auth import get_user_model
import pytest

@pytest.mark.django_db
class TestSignUpAPI:
  def test_signup_with_valid_data(self, api_client, user_payload_factory):
    response = api_client.post("/api/auth/register/", data=user_payload_factory(), format="json")

    assert response.status_code in [200,201]
