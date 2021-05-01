from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, ident, name, profile_pic, is_active=True):
        self.id = ident
        self.name = name
        self.profile_pic = profile_pic
        self.is_active = is_active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return True

    def update(self, name, profile_pic):
        self.name = name
        self.profile_pic = profile_pic
