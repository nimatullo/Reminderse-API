from datetime import datetime, timedelta
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    interval = Column(Integer, default=3)
    email_confirmed = Column(Boolean(), default=False)
    links = relationship(
        "Links", backref=backref("users"), lazy="dynamic", passive_deletes=True
    )
    text = relationship(
        "Text", backref=backref("users"), lazy="dynamic", passive_deletes=True
    )

    def __repr__(self):
        return "User('{0}', '{1}')".format(self.username, self.email)


def get_new_date():
    today = datetime.now()
    new_date = today + timedelta(days=3)
    return new_date


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)

    def __repr__(self):
        return "Category('{0}', '{1}')".format(self.id, self.title)


class Links(Base):

    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_title = Column(String(100), nullable=False)
    content = Column(String(300), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date = get_new_date()
    date_of_next_send = Column(Date, nullable=False, default=date)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", cascade="all,delete", backref=("links"))

    def __init__(
        self, entry_title, content, user_id, interval, category=None, date=None
    ) -> None:
        self.entry_title = entry_title
        self.content = content
        self.user_id = user_id
        self.category_id = category.id if category else None
        self.date_of_next_send = (
            date if date else datetime.now() + timedelta(days=interval)
        )

    def __repr__(self):
        return "Link('{0}', '{1}',)".format(self.entry_title, self.date_of_next_send)

    def json(self):
        return {
            "id": self.id,
            "entry_title": self.entry_title,
            "url": self.url,
            "date": str(self.date_of_next_send),
            "category": self.category if self.category else None,
        }


class Text(Base):
    __tablename__ = "text"
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    date = get_new_date()
    date_of_next_send = Column(Date, nullable=False, default=date)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship(
        "Category", cascade="all,delete", backref=backref("text", lazy="dynamic")
    )

    def __init__(
        self, entry_title, text_content, user_id, interval, category=None, date=None
    ) -> None:
        self.entry_title = entry_title
        self.content = text_content
        self.user_id = user_id
        self.category_id = category.id if category else None
        self.date_of_next_send = (
            date if date else datetime.now() + timedelta(days=interval)
        )

    def __repr__(self):
        return "Text('{0}', '{1}',)".format(self.entry_title, self.content)
