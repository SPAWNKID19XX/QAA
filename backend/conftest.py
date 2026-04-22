import pytest
from django.contrib.auth import get_user_model
from apps.accounts.tests.api.client import Client as APIClient
from rest_framework.test import APIClient

@pytest.fixture
def user_factory():
  # Here you can set up any necessary data for your tests, such as creating a new user in the 
  # database using ORM-Django
  counter = 0

  def create_user(**kwargs):
    nonlocal counter
    counter += 1
    
    data = {
      "username": f"factory_user_{counter}",
      "password": "testpass",
      "email": f"factory_email_{counter}@mail.com",
      "first_name": f"factory_fn{counter}",
      "last_name": f"factory_ln{counter}"
    }

    data.update(**kwargs)

    return get_user_model().objects.create_user(**data)

  return create_user

@pytest.fixture
def build_user():
  counter = 0

  def _build_user(**kwargs):
    nonlocal counter
    counter += 1

    data = {
      "username": f"build_user_{counter}",
      "password": "testpass",
      "first_name": f"build_fn{counter}",
      "last_name": f"build_ln{counter}",
      "email": f"build_user{counter}@mail.com",
    }
    data.update(**kwargs)
    return get_user_model() (
      **data
    )
  return _build_user

@pytest.fixture
def user_payload_factory():
  counter = 0

  def _user_payload_factory(**kwargs):
    nonlocal counter
    counter += 1
    user =  {
      "username": f"payload_user_{counter}",
      "password": "testpass123",
      "email": f"payload_email_{counter}@mail.com",
      "first_name": f"payload_fn{counter}",
      "last_name": f"payload_ln{counter}"
    }
    user.update(**kwargs)
    return user
  return _user_payload_factory


@pytest.fixture
def api_client():
  return APIClient()