from app.main import db
from .roles import Roles


class Employee(db.Model):

    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    role = db.relationship("Roles", backref="employee",
                           uselist=False)

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        if self.role:
            return "Employee :: {},  Role :: {} | {}".format(self.name, self.role.name, self.role.type)
        else:
            return "Employee :: {},  Role :: {} | {}".format(self.name, "None", "None")
