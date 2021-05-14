from flasktest.models import Users


def current_user(id):
    current_user_obj = Users.query.filter_by(id=id).first()
    return current_user_obj
