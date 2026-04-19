import requests

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def post(self, endpoint: str, json=None, headers=None):
        response = requests.post(f"{self.base_url}/{endpoint}/", json=json, headers=headers)
        return response
    
    def get(self, endpoint: str, headers=None):
        response = requests.get(f"{self.base_url}/{endpoint}/", headers=headers)
        return response