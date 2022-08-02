from sqlalchemy.orm import Session

from core.database.models import Category


def save(db: Session, data=None) -> bool:
    try:
        if data:
            db.add(data)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return False

    return True


def get_category_if_exists(db: Session, category_title: str) -> Category:
    category = db.query(Category).filter_by(title=category_title).first()
    return category


def add_new_category(db: Session, category_title: str) -> Category:
    category = Category(title=category_title)
    if save(db, category):
        return category
    return None


def get_category_by_id(db: Session, category_id: int) -> Category:
    category = db.query(Category).filter_by(id=category_id).first()
    return category
