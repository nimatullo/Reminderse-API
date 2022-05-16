from core.database.models import Links
from core.database import save


class LinkRepo:
    def __init__(self, db):
        self.db = db

    def create(self, title, url, current_user, category=None, date=None):
        if category is None:
            link = Links(
                entry_title=title,
                content=url,
                user_id=current_user["sub"],
                interval=current_user["interval"],
                date=date,
            )
        else:
            link = Links(
                entry_title=title,
                content=url,
                user_id=current_user["sub"],
                interval=current_user["interval"],
                category=category,
                date=date,
            )
        return save(self.db, link)
