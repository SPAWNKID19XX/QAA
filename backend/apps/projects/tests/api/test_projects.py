import pytest

from apps.projects.models import Project

@pytest.mark.django_db
class TestProjects:
  def test_post_new_projects_by_auth_userreturns_201(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "title": "Test Project",
      "description": "A test project",
      "status": "active"
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )

    assert response.status_code == 201
    assert response.data["title"] == "Test Project"
    assert response.data["description"] == "A test project"
    assert response.data["status"] == "active"
    assert response.data["owner"]['id'] == user.id
    
    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == "Test Project"
    assert db_project.description == "A test project"
    assert db_project.status == "active"
    assert db_project.owner.id == user.id

  def test_post_new_projects_with_blank_title_by_logged_user_returns_400(self, logged_in_user):
    client, user = logged_in_user
    
    project_data = {
      "title": "",
      "description": "A test project",
      "status": "active"
    }
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

  def test_post_new_projects_without_title_by_logged_user_returns_400(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "description": "A test project",
      "status": "active"
    }

    count_before = Project.objects.count()

    response = client.post(
      "/api/projects/",
      data=project_data,
      format="json"
    )
    response_data = response.json()
    count_after = Project.objects.count()
    assert response.status_code == 400
    assert "title" in response_data
    assert count_after == count_before

  def test_post_new_projects_with_blank_description_by_logged_user_returns_201(self, logged_in_user):
    client, user = logged_in_user
    
    project_data = {
      "title": "New Project",
      "description": "",
      "status": "active"
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == "New Project"
    assert response.data["description"] == ""
    assert response.data["status"] == "active"
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == "New Project"
    assert db_project.description == ""
    assert db_project.status == "active"
    assert db_project.owner.id == user.id

  def test_post_new_projects_without_description_by_logged_user_returns_201(self, logged_in_user):
    client, user = logged_in_user
    
    project_data = {
      "title": "New Project",
      "status": "active"
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == "New Project"
    assert response.data["description"] == ""
    assert response.data["status"] == "active"
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    assert db_project.title == "New Project"
    assert db_project.description == ""
    assert db_project.status == "active"
    assert db_project.owner.id == user.id

  def test_post_new_projects_without_status_by_logged_user_returns_201(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "title": "New Project",
      "description": "test project description",
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == "New Project"
    assert response.data["description"] == "test project description"
    assert response.data["status"] == "active"
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    
    assert db_project.title == "New Project"
    assert db_project.description == "test project description"
    assert db_project.status == "active"
    assert db_project.owner.id == user.id

  def test_post_new_projects_with_archived_status_by_logged_user_returns_201(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "title": "New Project",
      "description": "test project description",
      "status": "archived"
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 201
    assert response.data["title"] == "New Project"
    assert response.data["description"] == "test project description"
    assert response.data["status"] == "archived"
    assert response.data["owner"]['id'] == user.id

    db_project = Project.objects.get(id=response.data["id"])
    
    assert db_project.title == "New Project"
    assert db_project.description == "test project description"
    assert db_project.status == "archived"
    assert db_project.owner.id == user.id

  def test_post_new_projects_with_blank_status_by_logged_user_returns_400(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "title": "New Project",
      "description": "test project description",
      "status": ""
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 400
    assert "status" in response.data

  def test_post_new_projects_with_invalid_status_by_logged_user_returns_400(self, logged_in_user):
    client, user = logged_in_user

    project_data = {
      "title": "New Project",
      "description": "test project description",
      "status": "Invalid Status"
    }

    response = client.post(
      "/api/projects/", 
      data=project_data,
      format="json"
    )
    assert response.status_code == 400
    assert "status" in response.data
