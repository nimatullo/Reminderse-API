from datetime import date, timedelta

from flasktest.users.service.service import UserService
from flasktest.models import Category, Links, Text
from flasktest import db


def save(data=None):
    try:
        if data:
            db.session.add(data)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    finally:
        db.session.close()

    return True


def category_exists(category_title) -> Category:
    category = Category.query.filter_by(title=category_title).first()
    return category


def get_category_by_id(id) -> Category:
    category = Category.query.filter_by(id=id).first()
    return category


def get_category_by_title(title) -> Category:
    category = Category.query.filter_by(title=title).first()
    return category


def add_new_category(title) -> int:
    category = Category(title=title)
    if save(category):
        return category.id
    else:
        return -1


class TextRepo:
    def __init__(self) -> None:
        self.user_service = UserService()

    def add(self, title, content, category_id):
        text = Text(entry_title=title, text_content=content,
                    users=self.user_service.get_current_user(),
                    category_id=category_id)
        return save(text)

    def get_all_texts_for_user(self, user_id):
        return Text.query.filter_by(user_id=user_id)

    def home_page_texts(self, user_id):
        day = date.today() + timedelta(days=3)
        return Text.query.filter_by(user_id=user_id).filter(
            Text.date_of_next_send <= day
        )


class LinkRepo:
    def __init__(self) -> None:
        self.user_service = UserService()

    def add(self, title, url, category_id):
        link = Links(entry_title=title, url=url,
                     users=self.user_service.get_current_user(),
                     category_id=category_id)
        return save(link)

    def get_all_links_for_user(self, user_id):
        return Links.query.filter_by(user_id=user_id).all()

    def home_page_texts(self, user_id):
        day = date.today() + timedelta(days=3)
        return Links.query.filter_by(user_id=user_id).filter(
            Links.date_of_next_send <= day
        )

    def get_link(self, link_id) -> Links:
        return Links.query.filter_by(id=link_id).first()

    def update_entry_title(self, link_id, entry_title):
        link = self.get_link(link_id)
        link.entry_title = entry_title
        return save()

    def update_url(self, link_id, url):
        link = self.get_link(link_id)
        link.url = url
        return save()

    def update_category(self, link_id, category_id):
        link = self.get_link(link_id)
        link.category_id = category_id
        return save()

    def update_date(self, link_id, date):
        link = self.get_link(link_id)
        link.date_of_next_send = date
        return save()
