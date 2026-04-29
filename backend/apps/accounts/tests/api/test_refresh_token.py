import pytest

@pytest.mark.django_db
class TestRefreshToken:
  def test_get_access_with_valid_refresh_token_returns_200(self, user_payload_factory, api_client):
    user_response = api_client.post('/api/auth/register/', user_payload_factory(), format='json')
    user = user_response.json()['user']
    
    login_response = api_client.post(
      '/api/auth/login/', 
      {
        'username':user['username'],
        'password':'testpass123'
      },
      format='json'
    ).json()

    access = login_response['access']
    refresh = login_response['refresh']

    refresh_request= api_client.post(
      '/api/auth/token/refresh/', 
      {'refresh': refresh}, 
      HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    assert refresh_request.status_code == 200
    assert 'access' in refresh_request.json()
    assert 'refresh' not in refresh_request.json()
    assert len(refresh_request.json()['access']) > 0
    
    
  def test_get_access_without_refresh_in_body_returns_400(self, api_client,user_payload_factory):
    user_response = api_client.post('/api/auth/register/', user_payload_factory(), format='json')
    user = user_response.json()['user']
    
    login_response = api_client.post(
      '/api/auth/login/', 
      {
        'username':user['username'],
        'password':'testpass123'
      },
      format='json'
    ).json()

    access = login_response['access']

    refresh_request= api_client.post(
      '/api/auth/token/refresh/', 
      HHTTP_AUTHORIZATION=f"Bearer {access}"
    )

    assert refresh_request.status_code == 400
  
  def test_get_access_by_invalid_refresh_token_returns_401(self,api_client,user_payload_factory):
    user_response = api_client.post('/api/auth/register/', user_payload_factory(), format='json')
    user = user_response.json()['user']
    
    login_response = api_client.post(
      '/api/auth/login/', 
      {
        'username':user['username'],
        'password':'testpass123'
      },
      format='json'
    ).json()

    refresh = "invalid Refresh"

    refresh_request= api_client.post(
      '/api/auth/token/refresh/', 
      {'refresh':refresh}
    )

    assert refresh_request.status_code == 401
