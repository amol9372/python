from app.main.db_models.base_model import BaseModel
from app.main import db


class SharedLabels(BaseModel):

    __tablename__ = "shared_labels"

    user_label_id = db.Column(db.Integer, db.ForeignKey("user_labels.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    primary_user = db.Column(db.Boolean)

    def __init__(self, user_label_id, user_id, primary_user):
        self.user_id = user_id
        self.user_label_id = user_label_id
        self.primary_user = primary_user

    def __repr__(self) -> str:
        return "Shared Label with label_id ::: {} and user_id ::: {} and primary user ::: {}".format(self.user_label_id, self.user_id, self.primary_user)
