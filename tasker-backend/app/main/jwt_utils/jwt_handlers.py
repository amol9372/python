from ..models.user import user_pool, users

def authenticate(username, password):
    user = user_pool.UserPool.query.filter_by(email=username)
    if user and user_pool.UserPool.check_password(password_hash=user.password, password=password):
        return user


def identity(payload):
    user_id = payload['public_id']
    return users.User.get_user(user_id)
