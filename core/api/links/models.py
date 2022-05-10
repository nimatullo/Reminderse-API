from pydantic import BaseModel

class NewEntryRequest(BaseModel):
  entry_title: str
  content: str
  category: str
  date_of_next_send: str