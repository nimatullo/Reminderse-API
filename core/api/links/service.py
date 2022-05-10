from flask import json, make_response, jsonify
from core.api.links.models import NewEntryRequest
from core.api.links.repo import LinkRepo
from core.database import get_category_if_exists, add_new_category, get_category_by_id

# from core.entries.repo import get_category_by_id, get_category_by_title, category_exists, add_new_category
from datetime import date, timedelta, datetime


class LinkService:
    def __init__(self, db) -> None:
        self.repo = LinkRepo(db)
        self.db = db

    def get_link(self, link_id):
        link = self.repo.get_link(link_id)
        if not link:
            return make_response(jsonify({"message": "Link cannot be found"}), 404)

        category = get_category_by_id(link.category_id)

        if category:
            category = category.title
        else:
            category = ""

        return make_response(
            jsonify(
                {
                    "id": link.id,
                    "entry_title": link.entry_title,
                    "url": link.url,
                    "category": category,
                    "date": link.date_of_next_send,
                }
            ),
            200,
        )

    def pause_link(self, link_id):
        paused_date = date.today() - timedelta(days=1)
        link = self.repo.get_link(link_id)
        if self.repo.update_date(link, paused_date):
            return make_response(jsonify({"message": "Link paused"}), 200)
        else:
            return make_response(jsonify({"message": "Link does not exists"}), 404)

    def resume_link(self, link_id):
        resume_date = date.today() + timedelta(days=3)
        link = self.repo.get_link(link_id)
        if self.repo.update_date(link, resume_date):
            return make_response(jsonify({"message": "Link paused"}), 200)
        else:
            return make_response(jsonify({"message": "Link does not exists"}), 404)

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
        if newEntryRequest.category:
            category = get_category_if_exists(self.db, newEntryRequest.category)
            if not category:
                category = add_new_category(self.db, newEntryRequest.category)

            date_of_next_send = datetime.strptime(
                newEntryRequest.date_of_next_send, "%Y-%m-%d"
            )

            if self.repo.add(
                title=newEntryRequest.entry_title,
                url=validated_url,
                current_user=user,
                category=category,
                date=date_of_next_send,
            ):
                return {"message": "Link entry created"}
            else:
                raise Exception("Server error")
        else:
            if self.repo.add(
                title=entry_title, url=validated_url, date=date_of_next_send
            ):
                return make_response(jsonify({"message": "Link entry created"}), 201)
            else:
                return make_response(jsonify({"message": "Server error"}), 500)

    def update_link(self, link_id, user_id, new_title, new_url, new_category, new_date):
        link = self.repo.get_link(link_id)
        if not link:
            return make_response(jsonify({"message": "Link not found"}), 404)

        if not link.user_id == user_id:
            return make_response(jsonify({"message": "Unauthorized"}), 401)

        self.repo.update_entry_title(link, new_title)
        self.repo.update_url(link, new_url)
        self.repo.update_date(link, new_date)
        category = get_category_by_title(new_category)
        if not category:
            category = add_new_category(new_category)
        self.repo.update_category(link, category.id)
        return make_response(jsonify({"message": "Text updated"}), 200)

    def delete_link(self, link_id):
        if self.repo.delete_link(link_id):
            return make_response(jsonify({"message": "Link deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Link deletion failed"}), 404)

    def get_all(self, user_id):
        all_links = self.repo.get_all_links_for_user(user_id)
        response = [self.convert_link_to_dictionary(link) for link in all_links]
        return {"entries": response}

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
            "category": self.get_category_instance(self.db, link.category_id),
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
            return "https://"
