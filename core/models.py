from datetime import datetime, timedelta
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database.database import Base



class Users(Base):
    __tablename__ = 'users'
    id = Column(Text(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    interval = Column(Integer, default=3)
    email_confirmed = Column(Boolean(), default=False)
    links = relationship('Links', backref=backref(
        'users'), lazy='dynamic', passive_deletes=True)
    text = relationship('Text', backref=backref(
        'users'), lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "User('{0}', '{1}')".format(self.username, self.email)


def get_new_date():
    today = datetime.now()
    new_date = today + timedelta(days=3)
    return new_date

class Category(Base):
    __tablename__ = 'category'
    id = Column(Text(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(50), nullable=False)

    def __repr__(self):
        return "Category('{0}', '{1}')".format(self.id, self.title)

class Links(Base):

    __tablename__ = 'links'
    id = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entry_title = Column(String(100), nullable=False)
    url = Column(String(300), nullable=False)
    user_id = Column(String, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    date = get_new_date()
    date_of_next_send = Column(Date, nullable=False, default=date)
    category_id = Column(String, ForeignKey('category.id'))
    category = relationship(
        'Category', cascade="all,delete", backref=backref('links', lazy='dynamic'))

    def __init__(self, entry_title, url, users, category=None, date=None) -> None:
        self.entry_title = entry_title
        self.url = url
        self.user_id = users.id
        self.category_id = category.id if category else None
        self.date_of_next_send = date if date else datetime.now() + \
            timedelta(days=users.interval)

    def __repr__(self):
        return "Link('{0}', '{1}',)".format(self.entry_title, self.date_of_next_send)


class Text(Base):
    __tablename__ = 'text'
    id = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    entry_title = Column(String(100), nullable=False)
    text_content = Column(String(1000), nullable=False)
    date = get_new_date()
    date_of_next_send = Column(Date, nullable=False, default=date)
    user_id = Column(String, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(String, ForeignKey('category.id'))
    category = relationship(
        'Category', cascade="all,delete", backref=backref('text', lazy='dynamic'))

    def __init__(self, entry_title, text_content, users, category=None, date=None) -> None:
        self.entry_title = entry_title
        self.text_content = text_content
        self.user_id = users.id
        self.category_id = category.id if category else None
        self.date_of_next_send = date if date else datetime.now() + \
            timedelta(days=users.interval)

    def __repr__(self):
        return "Text('{0}', '{1}',)".format(self.entry_title, self.text_content)


