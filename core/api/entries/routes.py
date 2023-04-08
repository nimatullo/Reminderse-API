from fastapi import APIRouter, Depends

from core.database.database import get_db
from core.api.entries.service import EntryService

entries = APIRouter()


@entries.post("/send")
async def send_entries(db: get_db = Depends()):
    return EntryService(db).send_all_entries()
