from flask import json, make_response, jsonify
from core.api.links.models import NewEntryRequest, UpdateEntryRequest
from core.api.links.repo import LinkRepo
from core.api.response import response
from core.database import get_category_if_exists, add_new_category, get_category_by_id

# from core.entries.repo import get_category_by_id, get_category_by_title, category_exists, add_new_category
from datetime import date, timedelta, datetime


class LinkService:
    def __init__(self, db) -> None:
        self.repo = LinkRepo(db)
        self.db = db

    def get_link(self, link_id, user_id):
        link = self.repo.get_link(link_id, user_id)
        if not link:
            return response({"message": "Link not found"}, 404)
        return response(link, 200)

    def pause_link(self, link_id, current_user_id):
        paused_date = date.today() - timedelta(days=1)
        link = self.repo.get_link(link_id, current_user_id)

        if not link:
            return response({"message": "Link not found"}, 404)

        if self.repo.update_date(link, paused_date):
            return response({"message": "Link paused"}, 200)
        else:
            return response({"message": "Server error"}, 500)

    def resume_link(self, link_id, current_user_id):
        resume_date = date.today() + timedelta(days=3)
        link = self.repo.get_link(link_id, current_user_id)

        if not link:
            return response({"message": "Link not found"}, 404)

        if self.repo.update_date(link, resume_date):
            return response({"message": "Link resumed"}, 200)
        else:
            return response({"message": "Server error"}, 500)

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
        validated_date = self.validate_date(newEntryRequest.date_of_next_send)
        if newEntryRequest.category:
            category = get_category_if_exists(self.db, newEntryRequest.category)
            if not category:
                category = add_new_category(self.db, newEntryRequest.category)

            if self.repo.add(
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
            if self.repo.add(
                title=newEntryRequest.entry_title,
                url=validated_url,
                date=validated_date,
                current_user=user,
            ):
                return response({"message": "Link entry created"}, 201)
            else:
                return response({"message": "Server error"}, 500)

    def update_link(self, link_id, user_id, updateEntryRequest: UpdateEntryRequest):
        link = self.repo.get_link(link_id, user_id)
        if not link:
            return response({"message": "Link not found"}, 404)

        self.repo.update_entry_title(link, updateEntryRequest.entry_title)
        self.repo.update_url(link, updateEntryRequest.content)
        self.repo.update_date(link, updateEntryRequest.date_of_next_send)
        category = get_category_if_exists(self.db, updateEntryRequest.category)
        if not category:
            category = add_new_category(self.db, updateEntryRequest.category)
        self.repo.update_category(link, category.id)
        return response({"message": "Link updated"}, 200)

    def delete_link(self, link_id, current_user_id):
        if self.repo.delete_link(link_id, current_user_id):
            return response({"message": "Link deleted"}, 200)
        else:
            return response({"message": "Link deletion failed"}, 404)

    def get_all(self, user_id):
        all_links = self.repo.get_all_links_for_user(user_id)
        payload = [self.convert_link_to_dictionary(link) for link in all_links]
        return response({"entries": payload}, 200)

    def convert_text_to_dictionary(self, text):
        return {
            "id": text.id,
            "entry_title": text.entry_title,
            "content": text.content,
            "days": self.get_date_diff(text),
            "category": self.get_category_instance(self.db, text.category_id),
        }

    def convert_link_to_dictionary(self, link):
        return {
            "id": link.id,
            "entry_title": link.entry_title,
            "url": link.url,
            "days": self.get_date_diff(link),
            "category": link.category.title if link.category else None,
        }

    def get_category_instance(self, db, category_id):
        category = get_category_by_id(db, category_id)
        if category:
            return category.title
        else:
            return ""

    def get_date_diff(self, entry):
        date_diff = (entry.date_of_next_send - date.today()).days
        if date_diff == 0:
            return "Today"
        elif date_diff == 1:
            return "Tomorrow"
        else:
            return date_diff

    def validate_url(self, url):
        if "http" in url or "https" in url:
            return url
        else:
            return "https://" + url

    def validate_date(self, date):
        if date:
            return datetime.strptime(date, "%Y-%m-%d")
        else:
            return None
