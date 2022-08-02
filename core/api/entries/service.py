import validators
from core.api.entries.models import UpdateEntryRequest
from core.api.entries.repo import EntryRepo
from core.api.response import response
from core.database import get_category_if_exists, add_new_category, get_category_by_id

from datetime import date, timedelta


class EntryService:
    def __init__(self, db) -> None:
        self.repo = EntryRepo(db)
        self.db = db

    def get(self, id, user_id, model):
        entry = self.repo.get(model=model, id=id, user_id=user_id)
        if not entry:
            return response({"message": "Entry not found"}, 404)
        return response(self.to_json(entry), 200)

    def pause(self, model, id, user_id):
        paused_date = date.today() - timedelta(days=1)
        entry = self.repo.get(model=model, id=id, user_id=user_id)

        if not entry:
            return response({"message": "Entry not found"}, 404)

        if self.repo.update_date(entry, paused_date):
            return response({"message": "Entry paused"}, 200)
        else:
            return response({"message": "Server error"}, 500)

    def resume(self, model, id, user_id):
        resume_date = date.today() + timedelta(days=3)
        entry = self.repo.get(model=model, id=id, user_id=user_id)

        if not entry:
            return response({"message": "Entry not found"}, 404)

        if self.repo.update_date(entry, resume_date):
            return response({"message": "Entry resumed"}, 200)
        else:
            return response({"message": "Server error"}, 500)

    def update(self, model, id, user_id, updateEntryRequest: UpdateEntryRequest):
        entry = self.repo.get(model=model, id=id, user_id=user_id)
        if not entry:
            return response({"message": "Entry not found"}, 404)

        self.repo.update_entry_title(entry, updateEntryRequest.entry_title)
        self.repo.update_content(entry, updateEntryRequest.content)
        self.repo.update_date(entry, updateEntryRequest.date_of_next_send)
        category = get_category_if_exists(self.db, updateEntryRequest.category)
        if not category and updateEntryRequest.category != None:
            category = add_new_category(self.db, updateEntryRequest.category)
            self.repo.update_category(entry, category.id)
        return response({"message": "Entry updated"}, 200)

    def delete(self, model, id, user_id):
        if self.repo.delete(model=model, id=id, user_id=user_id):
            return response({"message": "Entry deleted"}, 200)
        else:
            return response({"message": "Server error"}, 500)

    def get_all(self, user_id, model):
        entries = self.repo.get_all_for_user(model=model, user_id=user_id)
        payload = [self.to_json(entry) for entry in entries]
        return response({"entries": payload}, 200)

    def to_json(self, entry):
        json = {
            "id": entry.id,
            "entry_title": entry.entry_title,
            "category": entry.category.title if entry.category else None,
            "date_of_next_send": entry.date_of_next_send,
        }
        if validators.url(entry.content):
            json["url"] = entry.content
        else:
            json["content"] = entry.content
        return json

    def get_date_diff(self, entry):
        date_diff = (entry.date_of_next_send - date.today()).days
        if date_diff < 0:
            return "Paused"
        elif date_diff == 0:
            return "Today"
        elif date_diff == 1:
            return "Tomorrow"
        else:
            return date_diff
