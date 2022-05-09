from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT

from core.api.auth.routes import auth
from core.api.users.routes import me
from core.config import settings

app = FastAPI()


@AuthJWT.load_config
def get_settings():
  return settings


app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(me, prefix="/me", tags=["user"])
