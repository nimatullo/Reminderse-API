import json
from core.api.users.service import UserService
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from core.api.users.repo import UserRepository

def user_authentication_headers(client: TestClient,email:str,  password: str):
  data = {
    "email": email,
    "password": password
  }
  r = client.post("/login", json.dumps(data))
  response = r.json()
  print(response)
  token = response["token"]
  headers = {"Authorization": f"Bearer {token}"}
  return headers 

def authentication_token_from_email(client: TestClient, email:str, db: Session):
  username:str = "test"
  password:str = "test"
  user = UserRepository(db).get_userinfo_email(email)
  if not user:
    user = UserService(db).signup(username, email, password)
  return user_authentication_headers(client, email, password)