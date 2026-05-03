import pytest
from apps.accounts.tests.helpers.data import make_string

from apps.projects.models import Project

@pytest.mark.django_db
class TestProjects:
  def test_post_new_projects_by_auth_user_returns_201(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory()

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )

    assert response.status_code == 201
    assert response.data["title"] == project_data["title"]
    assert response.data["description"] == project_data["description"]
    assert response.data["status"] == project_data["status"]
    assert response.data["owner"]['id'] == user.id
    
    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == project_data["title"]
    assert db_project.description == project_data["description"]
    assert db_project.status == project_data["status"]
    assert db_project.owner.id == user.id

  def test_post_new_projects_without_title_by_logged_user_returns_400(self, logged_in_user, project_payload_factory):
    client, _ = logged_in_user

    project_data = project_payload_factory()
    project_data.pop("title")

    count_before = Project.objects.count()

    response = client.post(
      "/api/projects/",
      data=project_data,
      format="json"
    )
    count_after = Project.objects.count()
    
    assert response.status_code == 400
    assert "title" in response.data
    assert count_after == count_before

  @pytest.mark.parametrize("title", ["", "  "], ids=["empty string", "spaces only"])
  def test_post_new_projects_with_blank_title_by_logged_user_returns_400(self, logged_in_user, project_payload_factory, title):
    client, _ = logged_in_user
    project_data = project_payload_factory(title=title)

    count_before = Project.objects.count()

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    count_after = Project.objects.count()
    
    assert response.status_code == 400
    assert "title" in response.data
    assert count_after == count_before

  @pytest.mark.parametrize("description, expected_description", [("  ", ""), ("", "")], ids=["empty string", "spaces only"])
  def test_post_new_projects_with_different_description_by_logged_user_returns_201(self, logged_in_user, project_payload_factory, description, expected_description):
    client, user = logged_in_user
    project_data = project_payload_factory(
      description=description
    )

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == project_data["title"]
    assert response.data["description"] == expected_description
    assert response.data["status"] == project_data["status"]
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == project_data["title"]
    assert db_project.description == expected_description
    assert db_project.status == project_data["status"]
    assert db_project.owner.id == user.id

  def test_post_new_projects_without_description_by_logged_user_returns_201(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory()
    project_data.pop("description")

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == project_data["title"]
    assert response.data["description"] == ""
    assert response.data["status"] == project_data["status"]
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == project_data["title"]
    assert db_project.description == ""
    assert db_project.status == project_data["status"]
    assert db_project.owner.id == user.id

  def test_post_new_projects_without_status_by_logged_user_returns_201(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory()
    project_data.pop("status")

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == project_data["title"]
    assert response.data["description"] == project_data["description"]  
    assert response.data["status"] == "active"
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    
    assert db_project.title == project_data["title"]
    assert db_project.description == project_data["description"]
    assert db_project.status == "active"
    assert db_project.owner.id == user.id

  @pytest.mark.parametrize("status", ["archived","active"], ids=["archived", "active"])
  def test_post_new_projects_with_archived_status_by_logged_user_returns_201(self, logged_in_user, project_payload_factory,status):
    client, user = logged_in_user
    project_data = project_payload_factory(status=status)

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == project_data["title"]
    assert response.data["description"] == project_data["description"]
    assert response.data["status"] == project_data["status"]
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    
    assert db_project.title == project_data["title"]
    assert db_project.description == project_data["description"]
    assert db_project.status == project_data["status"]
    assert db_project.owner.id == user.id

  @pytest.mark.parametrize("status", ["", "  ", "invalid status","ACTIVE"], ids=["empty string", "spaces only", "invalid value", "ACTIVE"])
  def test_post_new_projects_with_diferents_status_by_logged_user_returns_400(self, logged_in_user, project_payload_factory, status):

    client, _ = logged_in_user
    
    before_count = Project.objects.count()

    project_data = project_payload_factory(status=status)

    response = client.post(
      "/api/projects/", 
      data=project_data, 
      format="json"
    ) 

    after_count = Project.objects.count()
    
    assert response.status_code == 400
    assert "status" in response.data
    assert after_count == before_count

  def test_new_project_without_logged_user_returns_401(self, api_client, project_payload_factory):

    project_data = project_payload_factory()

    count_before = Project.objects.count()

    response = api_client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    count_after = Project.objects.count()
    
    assert response.status_code == 401
    assert "detail" in response.data
    assert count_after == count_before  

  @pytest.mark.parametrize(
      "title, expected_status_code", [
        (make_string(199), 201), 
        (make_string(200), 201), 
        (make_string(201), 400)], 
        ids=["199 characters", "200 characters", "201 characters"])
  def test_new_project_title_bundle_test(self, logged_in_user, project_payload_factory, title, expected_status_code):
    client, user = logged_in_user
    project_data = project_payload_factory(title=title)

    count_before = Project.objects.count()

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    count_after = Project.objects.count()
    
    assert response.status_code == expected_status_code

    if expected_status_code == 201:
      assert response.data["title"] == project_data["title"]
      assert response.data["description"] == project_data["description"]
      assert response.data["status"] == project_data["status"]
      assert response.data["owner"]['id'] == user.id
      assert count_before == count_after - 1

      db_project = Project.objects.get(id=response.data["id"])
      assert db_project.title == project_data["title"]
      assert db_project.description == project_data["description"]
      assert db_project.status == project_data["status"]
      assert db_project.owner.id == user.id
    else:
      assert count_before == count_after

  def test_new_project_submit_unother_owner(self, logged_in_user, project_payload_factory,user_payload_factory):
    client, user = logged_in_user
    other_user = user_payload_factory()
    project_data = project_payload_factory(owner=other_user)
    user_response = client.post("/api/auth/register/", data=other_user,format="json")
    
    assert user_response.status_code == 201

    
    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["owner"]['id'] == user.id
    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.owner.id == user.id
    