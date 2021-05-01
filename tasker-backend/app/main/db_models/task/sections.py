from sqlalchemy.orm import backref
from app.main import db
from app.main.db_models.base_model import BaseModel


class Section(BaseModel):

    __tablename__ = "sections"

    name = db.Column(db.Text)
    # One to many with Tasks
    tasks = db.relationship("Task", backref="section", lazy="dynamic")
    # Foreign key user_label_id
    user_label_id = db.Column(db.Integer, db.ForeignKey("user_labels.id"))

    def __init__(self, name, user_label_id):
        self.name = name
        self.user_label_id = user_label_id

    def create_section(section):
        db.session.add(section)
        db.session.commit()

    def __repr__(self) -> str:
        if self.tasks:
            return "Section with name ::: {} and tasks ::: {}".format(self.name, self.tasks)
        else:
            return "Section with name ::: {}".format(self.name)
