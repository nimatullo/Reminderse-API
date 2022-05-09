from pydoc import cli
from typing import Any, Generator
from pydantic import BaseModel


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#this is to include backend dir in sys.path so that we can import from db,main.py


from core.database.database import Base
from core.database.database import get_db
from core.api.auth.routes import auth
from core.api.users.routes import me
from tests.utils.users import authentication_token_from_email
from core.config import settings


def start_app():
  app = FastAPI()

  @AuthJWT.load_config
  def get_settings():
    return settings
  
  app.include_router(auth)
  app.include_router(me)
  return app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
  Base.metadata.create_all(engine)
  _app = start_app()
  yield _app
  Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
  connection = engine.connect()
  transaction = connection.begin()
  session = SessionTesting(bind=connection)
  yield session
  session.close()
  transaction.rollback()
  connection.close()

@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
  def _get_test_db():
    try:
      yield db_session
    finally:
      pass
  
  app.dependency_overrides[get_db] = _get_test_db
  yield TestClient(app)

@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: Session) -> Generator[dict, None, None]:
  return authentication_token_from_email(client=client, email="testing@reminderse.com", db=db_session)