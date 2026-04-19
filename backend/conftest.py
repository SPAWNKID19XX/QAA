import pytest
from django.contrib.auth import get_user_model
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
      "username": f"user_{counter}",
      "password": "testpass",
      "email": f"test_email_{counter}@mail.com",
      "first_name": f"test_fn{counter}",
      "last_name": f"test_ln{counter}"
    }

    data.update(**kwargs)

    return get_user_model().objects.create_user(**data)

  return create_user

@pytest.fixture
def build_user(**kwargs):
  counter = 0

  def _build_user(**kwargs):
    nonlocal counter
    counter += 1

    data = {
      "username": f"user_{counter}",
      "password": "testpass",
      "first_name": f"test_fn{counter}",
      "last_name": f"test_ln{counter}",
      "email": f"testuser{counter}@mail.com",
    }
    data.update(**kwargs)
    return get_user_model() (
      **data
    )
  return _build_user
