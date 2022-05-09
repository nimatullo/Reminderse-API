from core.models import Users
from sqlalchemy.orm import Session


class UserRepository():

    def __init__(self, db: Session):
        self.db = db

    def save(self, data=None):
        try:
            if data:
                self.db.add(data)
            self.db.commit()
        except Exception as e:
            print(f'Exception thrown during UserRepository save(): {e}')
            self.db.rollback()
            return False
        finally:
            print("Commiting save!")

        return True

    def add(self, username, email, password) -> bool:
        data = Users(username=username.lower().rstrip(),
                     password=password, email=email.lower())

        return self.save(data)

    def username_exists(self, username) -> bool:
        if self.db.query(Users).filter_by(username=username).first():
            return True
        else:
            return False

    def email_exists(self, email) -> bool:
        if self.db.query(Users).filter_by(email=email).first():
            return True
        else:
            return False

    def get_userinfo_id(self, user_id) -> Users:
        user = self.db.query(Users).filter_by(id=user_id).first()
        return user

    def get_userinfo_email(self, email) -> Users:
        return self.db.query(Users).filter_by(email=email).first()

    def change_username(self, user_id, new_username):
        user = self.db.query(Users).filter_by(id=user_id).first()
        user.username = new_username
        return self.save()

    def change_email(self, user_id, email):
        user = self.db.query(Users).filter_by(id=user_id).first()
        user.email = email
        user.email_confirmed = False
        return self.save()

    def change_password(self, id, password):
        user = self.db.query(Users).filter_by(id=id).first()
        user.password = password
        return self.save()

    def change_interval(self, interval, id):
        user = self.db.query(Users).filter_by(id=id).first()
        user.interval = interval
        return self.save()

    def set_email_to_confirmed(self, email) -> bool:
        user = self.db.query(Users).filter_by(email=email).first()
        user.email_confirmed = True
        return self.save()
