import pytest

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

  def test_post_new_projects_with_blank_title_by_logged_user_returns_400(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory(title="")

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

  def test_post_new_projects_without_title_by_logged_user_returns_400(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user

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

  def test_post_new_projects_with_blank_description_by_logged_user_returns_201(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory(
      description=""
    )

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

  def test_post_new_projects_with_archived_status_by_logged_user_returns_201(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory(status="archived")

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

  def test_post_new_projects_with_blank_status_by_logged_user_returns_400(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory(status="")
    
    before_count = Project.objects.count()
    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )

    after_count = Project.objects.count()
    assert response.status_code == 400
    assert "status" in response.data
    assert after_count == before_count

  def test_post_new_projects_with_invalid_status_by_logged_user_returns_400(self, logged_in_user, project_payload_factory):
    client, user = logged_in_user
    project_data = project_payload_factory(status="Invalid Status")

    before_count = Project.objects.count()

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    after_count = Project.objects.count()

    assert response.status_code == 400
    assert "status" in response.data
    assert after_count == before_count
