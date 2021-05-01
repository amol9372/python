from app.main import db
from app.main.db_models import user
from app.main.db_models.base_model import BaseModel

class UserLabel(BaseModel):

    __tablename__ = "user_labels"
    
    name = db.Column(db.Text)
    # one to many
    sections = db.relationship("Section", backref="label", lazy="dynamic")
    # foreign key user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    color = db.Column(db.Text)

    def __init__(self, name, user_id, color):
        self.name = name
        self.user_id = user_id
        self.color = color

    def create_user_label(label):
        db.session.add(label)
        db.session.commit()