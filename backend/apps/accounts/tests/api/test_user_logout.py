import pytest


@pytest.mark.django_db
class TestLogout:
  def test_user_logout_correct_credentials_205(self, api_client, user_payload_factory): 
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()
    
    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }
    
    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    access = log_user["access"]
    refresh = log_user["refresh"]

    logout_res = api_client.post("/api/auth/logout/",{"refresh": refresh}, format='json', HTTP_AUTHORIZATION=f"Bearer {access}" )
    assert logout_res.status_code == 205
    assert logout_res.content == b''

  def test_logout_without_refresh_returns_400(self, api_client, user_payload_factory):
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()
    
    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }
    
    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    access = log_user["access"]

    logout_res = api_client.post("/api/auth/logout/", format='json', HTTP_AUTHORIZATION=f"Bearer {access}" )

    assert logout_res.status_code == 400
    assert "detail" in logout_res.json()

  def test_logout_without_authorization_returns_401(self, api_client, user_payload_factory):
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()
    
    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }
    
    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    refresh = log_user["refresh"]
    logout_res = api_client.post("/api/auth/logout/", {"refresh":refresh}, format='json')
    
    assert logout_res.status_code == 401
    assert "detail" in logout_res.json()

  def test_logout_with_invalid_refresh_token_401(self, api_client, user_payload_factory):
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()

    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }

    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    refresh = "Invalid Refresh"
    access = log_user['access']
    logout_res = api_client.post("/api/auth/logout/", {"refresh":refresh}, format='json', HTTP_AUTHORIZATION=f"Bearer {access}")
    
    assert logout_res.status_code == 400
    assert "detail" in logout_res.json()

  def test_logout_reuse_refresh_token_401(self, api_client, user_payload_factory):
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()
    
    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }
    
    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    access = log_user['access']
    refresh = log_user['refresh']

    logout_res = api_client.post("/api/auth/logout/", {"refresh":refresh}, format='json', HTTP_AUTHORIZATION=f"Bearer {access}")
    
    reused_token_response = api_client.post("/api/auth/token/refresh/", {"refresh":refresh}, format='json')
    assert logout_res.status_code == 205
    assert reused_token_response.status_code == 401
    assert "detail" in reused_token_response.json()

  def test_user_double_logout_with_same_refresh_400(self, api_client, user_payload_factory): 
    user = api_client.post("/api/auth/register/", user_payload_factory(), format='json').json()
    
    log_data = {
      'username' : user['user']['username'],
      'password' : 'testpass123'
    }
    
    log_user = api_client.post("/api/auth/login/", {**log_data}, format='json').json()
    access = log_user["access"]
    refresh = log_user["refresh"]

    logout_res = api_client.post("/api/auth/logout/",{"refresh": refresh}, format='json', HTTP_AUTHORIZATION=f"Bearer {access}" )
    logout_res1 = api_client.post("/api/auth/logout/",{"refresh": refresh}, format='json', HTTP_AUTHORIZATION=f"Bearer {access}" )
    
    assert logout_res.status_code == 205
    assert logout_res1.status_code == 400

  @pytest.mark.parametrize("method",["get","put","patch"])
  def test_user_logout_invalid_methods_405(self,api_client , user_payload_factory,method):
    user = api_client.post('/api/auth/register/', user_payload_factory(), format='json').json()
    
    user_log_data = {
      "username": user['user']['username'],
      "password": "testpass123"
    }

    login_response = api_client.post('/api/auth/login/', user_log_data, format='json').json()

    access = login_response['access']

    response = getattr(api_client, method)("/api/auth/logout/", HTTP_AUTHORIZATION=f"Bearer {access}")

    assert response.status_code == 405
    assert 'detail' in response.json()