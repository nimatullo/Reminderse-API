import traceback
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from core.api.entries.models import NewEntryRequest, EntryResponse, UpdateEntryRequest
from core.api.links.service import LinkService
from core.api.schemas.generic_response import MessageResponse
from core.database.database import get_db
from core.api.entries.service import EntryService
from core.api.exceptions.RouteErrorHandler import RouteErrorHandler
from core.database.models import Links


links = APIRouter(route_class=RouteErrorHandler)


@links.post("/")
def add(
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
        return EntryService(db).get_all(model=Links, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.get("/{link_id}", response_model=EntryResponse)
def get(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).get(model=Links, id=link_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.delete("/{link_id}")
def delete(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).delete(model=Links, id=link_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.put("/{link_id}", response_model=MessageResponse)
def update(
    link_id: int,
    updateEntryRequest: UpdateEntryRequest,
    db: get_db = Depends(),
    Authenticate: AuthJWT = Depends(),
):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).update(
            model=Links,
            id=link_id,
            user_id=USER_ID,
            updateEntryRequest=updateEntryRequest,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@links.put("/{link_id}/pause", response_model=MessageResponse)
def pause(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).pause(model=Links, id=link_id, user_id=USER_ID)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@links.put("/{link_id}/resume", response_model=MessageResponse)
def resume(link_id: int, db: get_db = Depends(), Authenticate: AuthJWT = Depends()):
    Authenticate.jwt_required()
    try:
        USER_ID = Authenticate.get_jwt_subject()
        return EntryService(db).resume(model=Links, id=link_id, user_id=USER_ID)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
