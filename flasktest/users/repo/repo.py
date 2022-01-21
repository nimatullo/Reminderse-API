from flasktest.models import Users
from flasktest import db


class UserRepository():
    def save(self, data=None):
        try:
            if data:
                db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(f'Exception thrown during UserRepository save(): {e}')
            db.session.rollback()
            return False
        finally:
            print("Commiting save!")
            db.session.close()

        return True

    def add(self, username, email, password) -> bool:
        data = Users(username=username.lower().rstrip(),
                     password=password, email=email.lower())

        return self.save(data)

    def username_exists(self, username) -> bool:
        if Users.query.filter_by(username=username).first():
            return True
        else:
            return False

    def email_exists(self, email) -> bool:
        if Users.query.filter_by(email=email).first():
            return True
        else:
            return False

    def get_userinfo_id(self, user_id) -> Users:
        user = Users.query.filter_by(id=user_id).first()
        return user

    def get_userinfo_email(self, email) -> Users:
        return Users.query.filter_by(email=email).first()

    def change_username(self, user_id, new_username):
        user = Users.query.filter_by(id=user_id).first()
        user.username = new_username
        return self.save()

    def change_email(self, user_id, email):
        user = Users.query.filter_by(id=user_id).first()
        user.email = email
        user.email_confirmed = False
        return self.save()

    def change_password(self, id, password):
        user = Users.query.filter_by(id=id).first()
        user.password = password
        return self.save()

    def set_email_to_confirmed(self, email) -> bool:
        user = Users.query.filter_by(email=email).first()
        user.email_confirmed = True
        return self.save()
