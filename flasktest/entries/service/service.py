from nis import cat
from flask import json, make_response, jsonify
from sqlalchemy.sql.expression import text
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

        if (category):
            category = category.title
        else:
            category = ""
       

        return make_response(jsonify({
            "id": link.id,
            "entry_title": link.entry_title,
            "url": link.url,
            "category": category,
            "date": link.date_of_next_send
        }), 200)

    def get_text(self, text_id):
        text = self.text_repo.get_text(text_id)
        if not text:
            return make_response(jsonify({
                "message": "Text cannot be found"
            }), 404)

        category = get_category_by_id(text.category_id)

        return make_response(jsonify({
            "id": text.id,
            "entry_title": text.entry_title,
            "text_content": text.text_content,
            "category": category.title,
            "date": text.date_of_next_send
        }), 200)

    def pause_link(self, link_id):
        paused_date = date.today() - timedelta(days=1)
        link = self.link_repo.get_link(link_id)
        if self.link_repo.update_date(link, paused_date):
            return make_response(jsonify({
                "message": "Link paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Link does not exists"
            }), 404)

    def pause_text(self, text_id):
        paused_date = date.today() - timedelta(days=1)
        if self.text_repo.update_date(text_id, paused_date):
            return make_response(jsonify({
                "message": "Text paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Text does not exists"
            }), 404)

    def resume_link(self, link_id):
        resume_date = date.today() + timedelta(days=3)
        link = self.link_repo.get_link(link_id)
        if self.link_repo.update_date(link, resume_date):
            return make_response(jsonify({
                "message": "Link paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Link does not exists"
            }), 404)

    def resume_text(self, text_id):
        resume_date = date.today() + timedelta(days=3)
        if self.text_repo.update_date(text_id, resume_date):
            return make_response(jsonify({
                "message": "Text paused"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Text does not exists"
            }), 404)

    def add_link(self, entry_title, url, category_title):
        validated_url = self.validate_url(url)
        category = category_exists(category_title)
        if not category:
            add_new_category(category_title)
            category_id = category.id
            if not category_id:
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

    def add_text(self, entry_title, content, category_title):
        category = category_exists(category_title)
        category_id = 0;
        if not category:
            category = add_new_category(category_title)
            category_id = category.id
        if self.text_repo.add(entry_title, content, category_id):
            return make_response(jsonify({
                "message": "Text entry created"
            }), 201)
        else:
            return make_response(jsonify({
                "message": "Server error"
            }), 500)

    # DISGUSTING UPDATE METHOD. UPDATE NEEDED
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

        self.link_repo.update_entry_title(link, new_title)
        self.link_repo.update_url(link, new_url)
        self.link_repo.update_date(link, new_date)
        category = get_category_by_title(new_category)
        if not category:
            category = add_new_category(new_category)
        self.link_repo.update_category(link, category.id)
        return make_response(jsonify({
            "message": "Text updated"
        }), 200)

    def update_text(self, text_id, user_id, new_title, new_content, new_category, new_date):
        text = self.text_repo.get_text(text_id)
        if not text:
            return make_response(jsonify({
                "message": "Text not found"
            }), 404)

        if not text.user_id == user_id:
            return make_response(jsonify({
                "message": "Unauthorized"
            }), 401)

        self.text_repo.update_entry_title(text_id, new_title)
        self.text_repo.update_content(text_id, new_content)
        self.text_repo.update_date(text_id, new_date)
        category = get_category_by_title(new_category)
        if not category:
            category = add_new_category(new_category)
        self.text_repo.update_category(text_id, category.id)
        return make_response(jsonify({
            "message": "Text updated"
        }), 200)

    def delete_link(self, link_id):
        if self.link_repo.delete_link(link_id):
            return make_response(jsonify({
                "message": "Link deleted"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Link deletion failed"
            }), 404)

    def delete_text(self, text_id):
        if self.text_repo.delete_text(text_id):
            return make_response(jsonify({
                "message": "Text deleted"
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Text deletion failed"
            }), 404)

    def get_all_links(self, user_id):
        all_links = self.link_repo.get_all_links_for_user(user_id)
        response = [self.convert_link_to_dictionary(
            link) for link in all_links]
        return make_response(jsonify({
            "entries": response
        }), 200)

    def get_all_text(self, user_id):
        all_text = self.text_repo.get_all_texts_for_user(user_id)
        response = [self.convert_text_to_dictionary(
            link) for link in all_text]
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

    def convert_text_to_dictionary(self, text):
        return {
            "id": text.id,
            "entry_title": text.entry_title,
            "text_content": text.text_content,
            "days": self.get_date_diff(text),
            "category": self.get_category_instance(text.category_id)
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
