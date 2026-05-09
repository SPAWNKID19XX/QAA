import pytest

from apps.projects.models import Project

@pytest.mark.django_db
class TestAddNewMembersToProject:
  url = "/api/projects/"
  def test_add_new_members_to_project(self,user_factory, project_factory, logged_in_user):
    client, project_owner = logged_in_user
    user1 = user_factory()
    user2 = user_factory()
    user3 = user_factory()
    non_member_user = user_factory()

    project = project_factory(owner=project_owner)

    for user in [user1, user2, user3,]:
      response_add_users = client.post(
        f"{self.url}{project.id}/members/", 
        data={"user_id": user.id})
      assert response_add_users.status_code == 201

    response_get_members = client.get(f"{self.url}{project.id}/", format="json")
    assert response_get_members.status_code == 200
    
    project_members_data = response_get_members.data["members"]    
    assert len(project_members_data) == 3
    assert user1.id in project_members_data
    assert user2.id in project_members_data
    assert user3.id in project_members_data
    assert non_member_user.id not in project_members_data

    orm_project = Project.objects.get(id=project.id)
    assert orm_project.members.count() == 3
    assert not project.members.filter(id=non_member_user.id).exists()
    assert project.members.filter(id=user1.id).exists()
    assert project.members.filter(id=user2.id).exists()
    assert project.members.filter(id=user3.id).exists() 

