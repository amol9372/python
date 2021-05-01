from app.main import db
from app.main.models.base_model import BaseModel
from dataclasses import dataclass

@dataclass
class User(BaseModel):

    __tablename__ = "users"

    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    status = db.Column(db.Text)

    def __init__(self, name, email, status='ACTIVE'):
        self.name = name
        self.email = email
        self.status = status

    @staticmethod
    def create_user(user):
        db.session.add(user)
        # db.session.commit()

    def get_user(email):
        user = User.query.filter_by(email=email).first()
        return user

    def __repr__(self) -> str:
        return "User with id :: {}, name :: {}, email :: {}, status ::: {}".format(self.id, self.name, self.email, self.status

                                                                                   )
