from datetime import date, timedelta

from flasktest.users.service.service import UserService
from flasktest.models import Category, Links, Text
from flasktest import db


def save(data=None):
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def add(data):
    try:
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        return data
    except Exception as ex:
        print(f"Error saving data! {ex}")

    return None


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
    try:
        return add(category)
    except Exception:
        return -1


class TextRepo:
    def __init__(self) -> None:
        self.user_service = UserService()

    def add(self, title, content, category_id=None):
        if category_id == None:
            text = Text(entry_title=title, text_content=content,
                        users=self.user_service.get_current_user(),
                        )
        else:
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

    def get_text(self, text_id) -> Text:
        current_user = self.user_service.get_current_user()
        return Text.query.filter_by(id=text_id)\
            .filter_by(user_id=current_user.id)\
            .first()

    def delete_text(self, text_id):
        text = self.get_text(text_id)
        if not text:
            return False
        db.session.delete(text)
        return save()

    def update_entry_title(self, text_id, entry_title):
        text = self.get_text(text_id)
        text.entry_title = entry_title
        return save()

    def update_content(self, text_id, content):
        text = self.get_text(text_id)
        text.text_content = content
        return save()

    def update_category(self, text_id, category_id):
        text = self.get_text(text_id)
        text.category_id = category_id
        return save()

    def update_date(self, text_id, date):
        text = self.get_text(text_id)
        text.date_of_next_send = date
        return save()


class LinkRepo:
    def __init__(self) -> None:
        self.user_service = UserService()

    def add(self, title, url, category_id=None):
        if category_id == None:
            link = Links(entry_title=title, url=url,
                         users=self.user_service.get_current_user())
        else:
            link = Links(entry_title=title, url=url,
                         category_id=category_id)
        return save(link)

    def get_all_links_for_user(self, user_id):
        return Links.query.filter_by(user_id=user_id).all()

    def home_page_texts(self, user_id):
        day = date.today() + timedelta(days=3)
        return Links.query.filter_by(user_id=user_id).filter(
            Links.date_of_next_send <= day
        )

    def delete_link(self, link_id):
        link = self.get_link(link_id)
        if not link:
            return False
        db.session.delete(link)
        return save()

    def get_link(self, link_id) -> Links:
        current_user = self.user_service.get_current_user()
        return Links.query.filter_by(id=link_id)\
            .filter_by(user_id=current_user.id)\
            .first()

    def update_entry_title(self, link, entry_title):
        print(f"Updating entry {link.entry_title} to {entry_title}")
        link.entry_title = entry_title
        return save()

    def update_url(self, link, url):
        print(f"Updating URL from {link.url} to {url}")
        link.url = url
        return save()

    def update_category(self, link, category_id):
        link.category_id = category_id
        return save()

    def update_date(self, link: Links, date):
        link.date_of_next_send = date
        return save()
