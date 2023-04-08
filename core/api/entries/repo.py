from datetime import date, datetime, timedelta

from core.api.users.service import UserService
from core.database.models import Category, Links, Text, Users
from core.database import save
from sqlalchemy.orm import Session, joinedload


class EntryRepo:
    def __init__(self, db: Session) -> None:
        self.user_service = UserService(db)
        self.db = db

    def get_all_for_user(self, model, user_id):
        return (
            self.db.query(model)
            .options(joinedload(model.category))
            .filter(model.user_id == user_id)
            .all()
        )

    def get_all_for_today(self):
        today = date.today()
        links = (
            self.db.query(Links)
            .options(joinedload(Users.id))
            .filter(Links.date_of_next_send == today)
            .all()
        )
        texts = (
            self.db.query(Text)
            .options(joinedload(Users))
            .filter(Text.date_of_next_send == today)
            .all()
        )

        return links + texts

    def get(self, model, id, user_id):
        return (
            self.db.query(model)
            .options(joinedload(model.category))
            .filter(model.id == id)
            .filter(model.user_id == user_id)
            .first()
        )

    def delete(self, model, id, user_id):
        entry = self.get(model, id, user_id)
        if not entry:
            return False
        self.db.delete(entry)
        return save(self.db)

    def update_entry_title(self, entry, entry_title):
        if entry_title:
            entry.entry_title = entry_title
        return save(self.db)

    def update_content(self, entry, content):
        if content:
            entry.content = content
        return save(self.db)

    def update_category(self, entry, category_id):
        if category_id:
            entry.category_id = category_id
        return save(self.db)

    def update_date(self, entry, date):
        if date:
            entry.date_of_next_send = date
        return save(self.db)
