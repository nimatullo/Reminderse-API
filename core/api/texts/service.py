from core.database import get_category_by_id, add_new_category, get_category_if_exists
from core.api.utils import validate_date
from core.api.response import response
from core.api.entries.models import NewEntryRequest
from core.api.texts.repo import TextRepo


class TextService:
    def __init__(self, db) -> None:
        self.repo = TextRepo(db)
        self.db = db

    def add_text(self, newEntryRequest: NewEntryRequest, user: dict):
        validated_date = validate_date(newEntryRequest.date_of_next_send)
        if newEntryRequest.category:
            category = get_category_if_exists(self.db, newEntryRequest.category)
            if not category:
                category = add_new_category(self.db, newEntryRequest.category)

            if self.repo.create(
                title=newEntryRequest.entry_title,
                content=newEntryRequest.content,
                current_user=user,
                category=category,
                date=validated_date,
            ):
                return response({"message": "Text entry created"}, 201)
            else:
                raise Exception("Server error")
        else:
            if self.repo.create(
                title=newEntryRequest.entry_title,
                content=newEntryRequest.content,
                date=validated_date,
                current_user=user,
            ):
                return response({"message": "Text entry created"}, 201)
            else:
                return response({"message": "Server error"}, 500)
