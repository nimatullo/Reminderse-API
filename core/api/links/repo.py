from datetime import date, datetime, timedelta

from core.api.users.service import UserService
from core.models import Category, Links, Text, Users
from core.database import save
from sqlalchemy.orm import Session, joinedload


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

    def add(self, title, content, category=None, date=None):
        current_user = self.user_service.get_current_user()
        if category == None:
            text = Text(
                entry_title=title, text_content=content, date=date, users=current_user
            )
        else:
            text = Text(
                entry_title=title,
                text_content=content,
                users=current_user,
                category=category,
                date=date,
            )
        return add(text)

    def get_all_texts_for_user(self, user_id):
        return Text.query.filter_by(user_id=user_id)

    def home_page_texts(self, user_id):
        day = date.today() + timedelta(days=3)
        return Text.query.filter_by(user_id=user_id).filter(
            Text.date_of_next_send <= day
        )

    def get_text(self, text_id) -> Text:
        current_user = self.user_service.get_current_user()
        return (
            Text.query.filter_by(id=text_id).filter_by(user_id=current_user.id).first()
        )

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
    def __init__(self, db: Session) -> None:
        self.user_service = UserService(db)
        self.db = db

    def add(self, title, url, current_user, category=None, date=None):
        if category == None:
            link = Links(
                entry_title=title,
                url=url,
                user_id=current_user["sub"],
                interval=current_user["interval"],
                date=date,
            )
        else:
            link = Links(
                entry_title=title,
                url=url,
                user_id=current_user["sub"],
                interval=current_user["interval"],
                category=category,
                date=date,
            )
        return save(self.db, link)

    def get_all_links_for_user(self, user_id):
        return (
            self.db.query(Links)
            .options(
                joinedload(Links.category),
            )
            .filter(Links.user_id == user_id)
            .all()
        )
        # return self.db.query(Links).filter_by(user_id=user_id).join(Users).all()

    def home_page_texts(self, user_id):
        day = date.today() + timedelta(days=3)
        return Links.query.filter_by(user_id=user_id).filter(
            Links.date_of_next_send <= day
        )

    def delete_link(self, link_id: str, current_user_id: str) -> bool:
        link = self.get_link(link_id, current_user_id)
        if not link:
            return False
        self.db.delete(link)
        return save(self.db)

    def get_link(self, link_id, current_user_id) -> Links:
        return (
            self.db.query(Links)
            .filter_by(id=link_id)
            .filter_by(user_id=current_user_id)
            .options(joinedload(Links.category))
            .first()
        )

    def update_entry_title(self, link, entry_title):
        print(f"Updating entry {link.entry_title} to {entry_title}")
        link.entry_title = entry_title
        return save(self.db)

    def update_url(self, link, url):
        print(f"Updating URL from {link.url} to {url}")
        link.url = url
        return save(self.db)

    def update_category(self, link, category_id):
        link.category_id = category_id
        return save(self.db)

    def update_date(self, link: Links, date):
        link.date_of_next_send = date
        return save(self.db)
