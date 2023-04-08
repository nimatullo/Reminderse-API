from core.database.database import get_db
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from core.api.auth.models import LoginRequest, RegisterRequest, LoginResponse
from core.api.schemas.generic_response import MessageResponse
from core.api.users.service import UserService
from core.email.send_email import send_confirmation
from itsdangerous import URLSafeTimedSerializer
import traceback

ts = URLSafeTimedSerializer("super-secret-key")

auth = APIRouter()


@auth.post("/login", response_model=LoginResponse)
async def login(
    userPayload: LoginRequest, db: get_db = Depends(), Authorize: AuthJWT = Depends()
) -> LoginResponse:
    try:
        return UserService(db).login(userPayload.email, userPayload.password, Authorize)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@auth.post("/signup", response_model=MessageResponse)
async def signup(
    registerPayload: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: get_db = Depends(),
) -> MessageResponse:
    background_tasks.add_task(
        send_confirmation,
        registerPayload.email,
        {"token": ts.dumps(registerPayload.email, salt="email-confirmation-salt")},
    )
    try:
        return UserService(db).signup(
            registerPayload.username, registerPayload.email, registerPayload.password
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


@auth.delete("/logout", response_model=MessageResponse)
async def logout(db: get_db = Depends(), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        return UserService(db).logout(Authorize)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
