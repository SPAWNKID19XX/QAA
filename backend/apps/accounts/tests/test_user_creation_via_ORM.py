import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .helpers.data import make_string
from django.db import DataError

@pytest.mark.django_db
class TestORMUserCreation:
  def test_user_should_be_created_via_orm(self, existing_user):
    assert existing_user.id is not None
    assert existing_user.username == 'testuser'
    assert existing_user.email == 'test@example.com'

  def test_password_should_be_hashed(self, existing_user):
    assert existing_user.check_password('testpass')

  def test_user_should_not_be_created_with_existing_username(self, existing_user):
    with pytest.raises(IntegrityError):
      get_user_model().objects.create_user(
        username="testuser", 
        password="testpass"
      ) 

@pytest.mark.django_db
class TestUserFieldsValidation:
  def test_user_invalid_email_full_clean_validation_should_pass(self):
    with pytest.raises(ValidationError):
      user = get_user_model() (
          username="testuser1", 
          password="testpass",
          email="invalid-email"
        )
      user.full_clean()

  def test_user_username_below_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username=make_string(149), 
        password="testpass",
        first_name="test_first_name2"
      )
    user.full_clean()
    assert user.username == make_string(149)

  def test_user_username_at_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username=make_string(150), 
        password="testpass",
        first_name="test_first_name3"
      )
    user.full_clean()
    assert user.username == make_string(150)

  def test_user_username_above_max_length_full_clean_validation_should_fail(self):
    with pytest.raises(ValidationError):
      user = get_user_model()(
          username=make_string(151), 
          password="testpass",
          first_name="test_first_name4"
        )
      user.full_clean()      

  def test_user_first_name_below_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username="testuserbellow", 
        password="testpass",
        first_name=make_string(149)
      )
    user.full_clean()
    assert user.first_name == make_string(149)

  def test_user_first_name_at_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username="testuseratmax", 
        password="testpass",
        first_name=make_string(150)
      )
    user.full_clean()
    assert user.first_name == make_string(150)

  def test_user_first_name_above_max_length_full_clean_validation_should_fail(self):
    with pytest.raises(ValidationError):
      user = get_user_model()(
          username="testuserabove", 
          password="testpass",
          first_name=make_string(151)
        )
      user.full_clean()      
  
  def test_user_last_name_below_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username="testuserbellow2", 
        password="testpass",
        last_name=make_string(149)
      )
    user.full_clean()
    assert user.last_name == make_string(149)

  def test_user_last_name_at_max_length_full_clean_validation_should_pass(self):
    user = get_user_model().objects.create_user(
        username="testuseratmax2", 
        password="testpass",
        last_name=make_string(150)
      )
    user.full_clean()
    assert user.last_name == make_string(150)

  def test_user_last_name_above_max_length_full_clean_validation_should_fail(self):
    with pytest.raises(ValidationError):
      user = get_user_model()(
          username="testuserabove2", 
          password="testpass",
          last_name=make_string(151)
        )
      user.full_clean()      

  def test_user_username_duplicate_full_clean_validation_message_error_should_pass(self, existing_user):
    with pytest.raises(ValidationError) as exc_info:
      user = get_user_model()(
          username=existing_user.username, 
          password="testpass",
          email="test@example.com"
        )
      user.full_clean()
    assert 'username' in exc_info.value.message_dict
