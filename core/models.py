from datetime import datetime, timedelta
from email.policy import default

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=False), primary_key=True,
                   server_default=sqlalchemy.text("uuid_generate_v4()"))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    interval = db.Column(db.Integer, default=3)
    email_confirmed = db.Column(db.Boolean(), default=False)
    links = db.relationship('Links', backref=db.backref(
        'users'), lazy='dynamic', passive_deletes=True)
    text = db.relationship('Text', backref=db.backref(
        'users'), lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "User('{0}', '{1}')".format(self.username, self.email)


def get_new_date():
    today = datetime.now()
    new_date = today + timedelta(days=3)
    return new_date


class Links(db.Model):

    __tablename__ = 'links'
    id = db.Column(UUID(as_uuid=False), primary_key=True,
                   server_default=sqlalchemy.text("uuid_generate_v4()"))
    entry_title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    date = get_new_date()
    date_of_next_send = db.Column(db.Date, nullable=False, default=date)
    user_id = db.Column(UUID, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(UUID, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', cascade="all,delete", backref=db.backref('links', lazy='dynamic'))

    def __repr__(self):
        return "Link('{0}', '{1}',)".format(self.entry_title, self.date_of_next_send)


class Text(db.Model):
    __tablename__ = 'text'
    id = db.Column(UUID(as_uuid=False), primary_key=True,
                   server_default=sqlalchemy.text("uuid_generate_v4()"))
    entry_title = db.Column(db.String(100), nullable=False)
    text_content = db.Column(db.String(1000), nullable=False)
    date = get_new_date()
    date_of_next_send = db.Column(db.Date, nullable=False, default=date)
    user_id = db.Column(UUID, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(UUID, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', cascade="all,delete", backref=db.backref('text', lazy='dynamic'))

    def __repr__(self):
        return "Text('{0}', '{1}',)".format(self.entry_title, self.text_content)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(UUID(as_uuid=False), primary_key=True,
                   server_default=sqlalchemy.text("uuid_generate_v4()"))
    title = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "Category('{0}', '{1}')".format(self.id, self.title)
