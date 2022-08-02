from core.api.links.repo import LinkRepo
from core.api.entries.models import NewEntryRequest
from core.database import get_category_if_exists, add_new_category
from core.api.response import response
from core.api.utils import validate_date


class LinkService:
    def __init__(self, db):
        self.repo = LinkRepo(db)
        self.db = db

    def add_link(self, newEntryRequest: NewEntryRequest, user: dict):
        """
        Cases:
            1. Category is provided
                a. Category exists
                    - Get category
                    - Save link
                b. Category does not exist
                    - Create category
                    - Save link
            2. Category is not provided
                - Save link
        """
        validated_url = self.validate_url(newEntryRequest.content)
        validated_date = validate_date(newEntryRequest.date_of_next_send)
        if newEntryRequest.category:
            category = get_category_if_exists(self.db, newEntryRequest.category)
            if not category:
                category = add_new_category(self.db, newEntryRequest.category)

            if self.repo.create(
                title=newEntryRequest.entry_title,
                url=validated_url,
                current_user=user,
                category=category,
                date=validated_date,
            ):
                return response({"message": "Link entry created"}, 201)
            else:
                raise Exception("Server error")
        else:
            if self.repo.create(
                title=newEntryRequest.entry_title,
                url=validated_url,
                date=validated_date,
                current_user=user,
            ):
                return response({"message": "Link entry created"}, 201)
            else:
                return response({"message": "Server error"}, 500)

    def validate_url(self, url):
        if "http" in url or "https" in url:
            return url
        else:
            return "https://" + url
