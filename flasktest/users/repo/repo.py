from flasktest.models import Users
from flasktest import db


class UserRepository():
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

    def get_userinfo_id(self, id) -> Users:
        return Users.query.filter_by(id=id).first()

    def get_userinfo_email(self, email) -> Users:
        return Users.query.filter_by(email=email).first()

    def change_username(self, id, new_username):
        user = self.get_userinfo_id(id)
        user.username = new_username
        return self.save()

    def change_email(self, id, email):
        user = self.get_userinfo_id(id)
        user.email = email
        user.email_confirmed = False
        return self.save()

    def change_password(self, id, password):
        user = self.get_userinfo_id(id)
        user.password = password
        return self.save()

    def set_email_to_confirmed(self, email) -> bool:
        user = self.get_userinfo_email(email)
        user.email_confirmed = True
        return self.save()
