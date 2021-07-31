from flasktest.entries.service.service import EntryService
import uuid
from datetime import timedelta, date

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from flasktest import daily_email
from flasktest import db
from flasktest.entries.utils import add_link_to_db, add_text_to_db, category_exists, get_all_links, get_all_texts, \
    generate_links_dict, generate_text_dict
from flasktest.users.service.service import UserService
from flasktest.models import Links, Category, Text

entries = Blueprint('entries', __name__)
service = EntryService()
user_service = UserService()


@entries.route("/api/link/add", methods=["POST"])
@jwt_required
def add_link():
    if request.is_json:
        entry_title = request.json.get('entry_title')
        url = request.json.get('url')
        category = request.json.get('category')

        return service.add_link(entry_title, url, category)


@entries.route("/api/text/add", methods=["POST"])
@jwt_required
def add_text():
    entry_title = request.json.get('entry_title')
    text_content = request.json.get('text_content')
    category = request.json.get('category')

    return service.add_text(entry_title, text_content, category)


@entries.route('/api/link/list', methods=['GET'])
@jwt_required
def all_links():
    CURRENT_USER = user_service.get_current_user()
    return service.get_all_links(CURRENT_USER.id)


@entries.route('/api/text/list', methods=['GET'])
@jwt_required
def all_texts():
    CURRENT_USER = user_service.get_current_user()
    return service.get_all_text(CURRENT_USER.id)


@entries.route("/api/link/<link_id>", methods=["PUT"])
@jwt_required
def edit_link_api(link_id):
    CURRENT_USER = user_service.get_current_user()
    entry_title = request.json.get('entry_title')
    url = request.json.get('url')
    category = request.json.get('category')
    date = request.json.get('date')
    return service.update_link(link_id,
                               CURRENT_USER.id,
                               entry_title,
                               url,
                               category,
                               date)


@entries.route("/api/text/<text_id>", methods=["PUT"])
@jwt_required
def edit_text_api(text_id):
    CURRENT_USER = user_service.get_current_user()
    entry_title = request.json.get('entry_title')
    text_content = request.json.get('text_content')
    category = request.json.get('category')
    date = request.json.get('date')
    return service.update_text(text_id,
                               CURRENT_USER.id,
                               entry_title,
                               text_content,
                               category,
                               date)


@entries.route('/api/link/<link_id>', methods=['GET'])
@jwt_required
def get_link(link_id):
    return service.get_link(link_id)


@entries.route('/api/text/<text_id>', methods=['GET'])
@jwt_required
def get_text(text_id):
    return service.get_text(text_id)


@entries.route('/api/link/<link_id>/pause', methods=["PUT"])
@jwt_required
def pause_link(link_id):
    return service.pause_link(link_id)


@entries.route('/api/text/<text_id>/pause', methods=["PUT"])
@jwt_required
def pause_text(text_id):
    return service.pause_text(text_id)


@entries.route('/api/link/<link_id>/resume', methods=["PUT"])
@jwt_required
def resume_link(link_id):
    return service.resume_link(link_id)


@entries.route('/api/text/<text_id>/resume', methods=["PUT"])
@jwt_required
def resume_text(text_id):
    return service.resume_text(text_id)


@entries.route('/api/link/<link_id>', methods=['DELETE'])
@jwt_required
def delete_link(link_id):
    return service.delete_link(link_id)


@entries.route('/api/text/<text_id>', methods=['DELETE'])
@jwt_required
def delete_text(text_id):
    return service.delete_text(text_id)


@entries.route('/api/entries/send', methods=["POST"])
def send_entries():
    emails_sent = daily_email.send_to_each_user()
    email_list = []
    for user in emails_sent:
        email_list.append({
            "email": user.email,
            "username": user.username
        })
    return make_response(
        jsonify({
            "data": "EMAILS SENT SUCCESSFULLY",
            "number_of_emails": f'{len(emails_sent)} emails sent.',
            "email_list": email_list
        })
    )
