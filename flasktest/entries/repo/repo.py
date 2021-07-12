from flasktest.users import service
from flasktest.users.service.service import UserService
from flasktest.models import Category, Text
from flasktest import db


class TextRepo:
    def __init__(self) -> None:
        self.user_service = UserService()

    def save(self, data=None):
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

    def add(self, title, content, category_id):
        text = Text(entry_title=title, text_content=content,
                    users=self.user_service.get_current_user(),
                    category_id=category_id)
        return self.save(text)

    def category_exists(self, category_title):
        category = Category.query.filter_by(title=category_title).first()
        return category is not None


class LinkRepo:
    def __init__(self) -> None:
        self.user_service = UserService()
