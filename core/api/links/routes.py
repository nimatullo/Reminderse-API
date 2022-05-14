import traceback
from click import echo
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from core.api.links.models import NewEntryRequest, EntryResponse
from core.api.schemas.generic_response import MessageResponse
from core.database.database import get_db
from core.api.links.service import LinkService
from core.api.exceptions.RouteErrorHandler import RouteErrorHandler


links = APIRouter(route_class=RouteErrorHandler)


@links.post("/")
def add_link(
    newEntryRequest: NewEntryRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
):
    Authenticate.jwt_required()
    try:
        USER = Authenticate.get_raw_jwt()
        return LinkService(db).add_link(newEntryRequest, USER)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@links.get("/")
def get_all(db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return LinkService(db).get_all(USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.get("/{link_id}", response_model=EntryResponse)
def get(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return LinkService(db).get_link(link_id, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.put("/{link_id}/pause", response_model=MessageResponse)
def pause_link(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return LinkService(db).pause_link(link_id, USER_ID)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@links.put("/{link_id}/resume", response_model=MessageResponse)
def resume_link(
    link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()
):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return LinkService(db).resume_link(link_id, USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
