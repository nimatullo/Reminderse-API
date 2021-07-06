from flasktest.models import Users


def current_user(user_id):
    current_user_obj = Users.query.filter_by(id=user_id).first()
    return current_user_obj
