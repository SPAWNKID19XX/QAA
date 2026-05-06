import pytest
import random

@pytest.mark.django_db
class TestProjectsGet:
  url = "/api/projects/"

  def test_get_projects_response_structure(self, user_factory, logged_in_user, project_factory):
    client, user = logged_in_user
    n_projects = random.randint(5, 15)

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
    print(response.data)

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