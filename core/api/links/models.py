from typing import Optional
from pydantic import BaseModel


class NewEntryRequest(BaseModel):
    entry_title: str
    content: str
    category: Optional[str] = None
    date_of_next_send: Optional[str] = None


class EntryResponse(BaseModel):
    entry_title: str
    content: str
    category: Optional[str] = None
    date_of_next_send: Optional[str] = None


class UpdateEntryRequest(BaseModel):
    entry_title: Optional[str]
    content: Optional[str]
    category: Optional[str] = None
    date_of_next_send: Optional[str] = None
