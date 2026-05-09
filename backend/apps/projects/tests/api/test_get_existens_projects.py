import pytest

@pytest.mark.django_db
class TestProjectsGet:
  url = "/api/projects/"

  def test_get_projects_response_structure(self, logged_in_user, project_factory):
    client, user = logged_in_user

    for _ in range(3):
      project_factory(owner=user)
    
    response = client.get(self.url)

    assert response.status_code == 200
    assert 'count' in response.data
    assert response.data['count'] == 3
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data
    assert isinstance(response.data['results'], list)
    assert len(response.data['results']) == 3

  def test_get_projects_data_integrity(self, logged_in_user, project_factory):
    client, user = logged_in_user
    new_project = project_factory(owner=user)
    response = client.get(self.url)

    assert response.status_code == 200
    response_data = response.data['results'][0]
    assert response_data['id'] is not None
    assert new_project.id == response_data['id']
    assert new_project.title == response_data['title']
    assert new_project.description == response_data['description']
    assert new_project.status == response_data['status']
    assert new_project.owner.id == response_data['owner']['id']
    assert new_project.owner.username == response_data['owner']['username']
    assert "members_count" in response_data
    assert "project_members" not in response_data
    assert "updated_at" not in response_data

  def test_get_projects_owner_data_integrity(self, logged_in_user, project_factory):
    client, user = logged_in_user
    new_project = project_factory(owner=user)
    response = client.get(self.url)

    assert response.status_code == 200
    response_data = response.data['results'][0]

    assert response_data['owner']['id'] is not None
    assert response_data['owner']['username'] is not None
    assert len(response_data['owner']) == 2
    assert response_data['owner']['id'] == new_project.owner.id
    assert response_data['owner']['username'] == new_project.owner.username

  def test_get_projects_only_matching_projects_filter(self, logged_in_user, project_factory, user_factory):
    client, user = logged_in_user
    another_user = user_factory()
    project1 = project_factory(owner=user, status="active")
    project2 = project_factory(owner=user, status="archived")
    project3 = project_factory(owner=user, status="active")
    project4 = project_factory(owner=another_user, status="active")

    response_act = client.get(self.url, {"status": "active"}) 
    assert response_act.status_code == 200

    project_ids_act = {proj['id'] for proj in response_act.data['results']}
    assert project4.id not in project_ids_act
    
    assert all(obj["status"] == "active" for obj in response_act.data['results'])
    assert response_act.data['count'] == 2
    assert len(response_act.data['results']) == 2
    assert project1.id in project_ids_act
    assert project3.id in project_ids_act
    assert project2.id not in project_ids_act

    response_arh = client.get(self.url, {"status": "archived"})
    assert response_arh.status_code == 200
    
    project_ids_arh = {proj['id'] for proj in response_arh.data['results']}

    assert all(obj["status"] == "archived" for obj in response_arh.data['results'])
    assert response_arh.data['count'] == 1
    assert len(response_arh.data['results']) == 1
    assert project2.id in project_ids_arh
    assert project1.id not in project_ids_arh
    assert project3.id not in project_ids_arh

  def test_get_projects_pagination(self, logged_in_user, project_factory):
    client, user = logged_in_user

    for _ in range(15):
      project_factory(owner=user)

    response = client.get(self.url) 
    assert response.status_code == 200
    assert response.data['count'] == 15
    assert len(response.data['results']) == 10
    assert response.data['next'] is not None
    assert response.data['previous'] is None

    next_url = response.data['next']
    response_next = client.get(next_url)
    assert response_next.data["count"] == 15
    assert response_next.status_code == 200
    assert len(response_next.data['results']) == 5
    assert response_next.data['next'] is None
    assert response_next.data['previous'] is not None
    
    response_p2 = client.get(self.url, {"page": "2"})
    assert response_p2.status_code == 200
    assert response_p2.data["count"] == 15
    assert len(response_p2.data['results']) == 5
    assert response_p2.data['next'] is None
    assert response_p2.data['previous'] is not None
