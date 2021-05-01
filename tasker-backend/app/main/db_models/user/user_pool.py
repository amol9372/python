from app.main import db
from werkzeug.security import check_password_hash, generate_password_hash

from app.main.models.base_model import BaseModel


class UserPool(BaseModel):
    __tablename__ = "user_pool"

    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    provider = db.Column(db.Text)

    def __init__(self, name, email, password, provider):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.provider = provider

    @classmethod
    def check_password(self, password_hash, password):
        return check_password_hash(password_hash, password)

    @classmethod
    def register_user_in_pool(self, user_pool):
        db.session.add(user_pool)
        # db.session.commit() 
    
    @classmethod
    def get_user_from_pool(self, email):
        user = UserPool.query.filter_by(email=email).first()
        return user

    def __repr__(self) -> str:
        return "User with id :: {}, name :: {}, email :: {}, provider ::: {}".format(
            self.id, self.name, self.email, self.provider
        )
