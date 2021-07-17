from flask import json, make_response, jsonify
from flasktest.entries.repo.repo import LinkRepo, TextRepo, get_category_by_id
from flasktest.entries.repo.repo import get_category_by_id, get_category_by_title, category_exists, add_new_category
from datetime import date, timedelta


class EntryService:
    def __init__(self) -> None:
        self.link_repo = LinkRepo()
        self.text_repo = TextRepo()

    def get_link(self, link_id):
        link = self.link_repo.get_link(link_id)
        if not link:
            return make_response(jsonify({
                "message": "Link cannot be found"
            }), 404)

        category = get_category_by_id(link.category_id)

        return make_response(jsonify({
            "id": link.id,
            "entry_title": link.entry_title,
            "url": link.url,
            "category": category,
            "date": link.date_of_next_send
        }), 200)

    def pause_link(self, link_id):
        paused_date = date.today() - timedelta(days=1)
        if self.link_repo.update_date(link_id, paused_date):
            return make_response(jsonify({
                "message": "Link paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Link does not exists"
            }), 404)

    def resume_link(self, link_id):
        resume_date = date.today + timedelta(days=3)
        if self.link_repo.update_date(link_id, resume_date):
            return make_response(jsonify({
                "message": "Link paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Link does not exists"
            }), 404)

    def add_link(self, entry_title, url, category_title):
        validated_url = self.validate_url(url)
        category_id = 0
        if category_exists(category_title):
            category_id = get_category_by_title(category_title).id
        else:
            category_id = add_new_category(category_title)
            if category_id < 0:
                return make_response(jsonify({
                    "message": "Server error"
                }), 500)
        if self.link_repo.add(entry_title, validated_url, category_id):
            return make_response(jsonify({
                "message": "Link entry created"
            }), 201)
        else:
            return make_response(jsonify({
                "message": "Server error"
            }), 500)

    def update_link(self, link_id, user_id, new_title, new_url, new_category, new_date):
        link = self.link_repo.get_link(link_id)
        if not link:
            return make_response(jsonify({
                "message": "Link not found"
            }), 404)

        if not link.user_id == user_id:
            return make_response(jsonify({
                "message": "Unauthorized"
            }), 401)

        self.link_repo.update_entry_title(link_id, new_title)
        self.link_repo.update_url(link_id, new_url)
        self.link_repo.update_date(link_id, new_date)
        category = get_category_by_title(new_category)
        if not category:
            category = add_new_category(new_category)
        self.link_repo.update_category(link_id, category.id)
        return make_response(jsonify({
            "message": "Link updated"
        }), 200)

    def delete_link(self, link_id):
        if self.link_repo.delete_link(link_id):
            return make_response(jsonify({
                "message": "Link deletion failed"
            }), 404)
        else:
            return make_response(jsonify({
                "message": "Link deleted"
            }), 200)

    def get_all_links(self, user_id):
        all_links = self.link_repo.get_all_links_for_user(user_id)
        response = [self.convert_link_to_dictionary(
            link) for link in all_links]
        return make_response(jsonify({
            "entries": response
        }), 200)

    def convert_text_to_dictionary(self, text):
        return {
            "id": text.id,
            "entry_title": text.entry_title,
            "content": text.content,
            "days": self.get_date_diff(text),
            "category": self.get_category_instance(text.category_id)
        }

    def convert_link_to_dictionary(self, link):
        return {
            "id": link.id,
            "entry_title": link.entry_title,
            "url": link.url,
            "days": self.get_date_diff(link),
            "category": self.get_category_instance(link.category_id)
        }

    def get_category_instance(self, category_id):
        category = get_category_by_id(category_id)
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
