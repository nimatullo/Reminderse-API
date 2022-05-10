from typing import Optional
from pydantic import BaseModel


class NewEntryRequest(BaseModel):
    entry_title: str
    content: str
    category: Optional[str] = None
    date_of_next_send: Optional[str] = None
