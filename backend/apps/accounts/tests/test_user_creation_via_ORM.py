import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .helpers.data import make_string

@pytest.mark.django_db
class TestORMUserCreation:
  def test_user_should_be_created_via_orm(self, user_factory):
    user = user_factory(username="testuser", email="testuser@example.com")
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"

  def test_password_should_be_hashed(self, user_factory):
    user = user_factory()
    assert user.check_password('testpass')

  def test_user_should_not_be_created_with_existing_username(self, user_factory):
    user_factory(username="borisisac")
    with pytest.raises(IntegrityError):
      user_factory(
        username="borisisac"
      ) 



@pytest.mark.django_db
class TestUserFieldsValidation:

  def test_invalid_email_full_clean_fail(self, build_user):
    with pytest.raises(ValidationError):
      user = build_user (
          email="invalid-email"
        )
      user.full_clean()

  def test_user_username_below_max_length_full_clean_validation(self, build_user):
    user = build_user (
        username=make_string(149), 
      )
    user.full_clean()
    assert user.username == make_string(149)

  def test_user_username_at_max_length_full_clean_validation(self, build_user):
    user = build_user (
        username=make_string(150), 
      )
    user.full_clean()
    assert user.username == make_string(150)

  def test_user_username_above_max_length_full_clean_validation(self, build_user):
    with pytest.raises(ValidationError):
      user = build_user(
          username=make_string(151), 
        )
      user.full_clean()      

  def test_user_first_name_below_max_length_full_clean_validation(self, build_user):
    user = build_user (
        first_name=make_string(149)
      )
    user.full_clean()
    assert user.first_name == make_string(149)

  def test_user_first_name_at_max_length_full_clean_validation(self, build_user):
    user = build_user (
        first_name=make_string(150)
      )
    user.full_clean()
    assert user.first_name == make_string(150)

  def test_user_first_name_above_max_length_full_clean_validation(self, build_user):
    with pytest.raises(ValidationError):
      user = build_user(
          first_name=make_string(151)
        )
      user.full_clean()      

  def test_user_last_name_below_max_length_full_clean_validation(self, build_user):
    user = build_user (
        last_name=make_string(149)
      )
    user.full_clean()
    assert user.last_name == make_string(149)

  def test_user_last_name_at_max_length_full_clean_validation(self, build_user):
    user = build_user (
        last_name=make_string(150)
      )
    user.full_clean()
    assert user.last_name == make_string(150)

  def test_user_last_name_above_max_length_full_clean_validation(self, build_user):
    with pytest.raises(ValidationError):
      user = build_user(
          last_name=make_string(151)
        )
      user.full_clean()      

  def test_username_duplicate_has_message_error(self, user_factory, build_user):
    existing_user = user_factory(username="existinguser")
    with pytest.raises(ValidationError) as exc_info:
      user = build_user(
          username=existing_user.username, 
        )
      user.full_clean()
    assert 'username' in exc_info.value.message_dict
