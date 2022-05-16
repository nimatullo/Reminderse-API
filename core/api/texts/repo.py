from sqlalchemy.orm import Session

from core.api.users.service import UserService
from core.database.models import Text
from core.database import save


class TextRepo:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, title, content, current_user, category=None, date=None):
        if category == None:
            text = Text(
                entry_title=title,
                text_content=content,
                date=date,
                user_id=current_user["sub"],
                interval=current_user["interval"],
            )
        else:
            text = Text(
                entry_title=title,
                text_content=content,
                user_id=current_user["sub"],
                interval=current_user["interval"],
                category=category,
                date=date,
            )
        return save(self.db, text)
