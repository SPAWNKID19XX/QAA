import pytest
from django.contrib.auth import get_user_model

@pytest.fixture(scope='function')
def existing_user():
  # Here you can set up any necessary data for your tests, such as creating a new user in the 
  # database using ORM-Django
  
  # For example:
  # user = User.objects.create_user(username='testuser', password='testpass')
  # return user
  user = get_user_model().objects.create_user(
    username="testuser", 
    password="testpass",
    first_name="test_fn",
    last_name="test_ln",
    email="test@example.com",
    is_staff = True,
    is_active = True
  )
  return user