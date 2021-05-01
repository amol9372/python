from app.main import db
from .employee import employee


class Roles(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    employee_id = db.Column(
        db.Integer, db.ForeignKey("employee.id"), nullable=True)

    def __init__(self, name, type, employee_id) -> None:
        self.name = name
        self.type = type
        self.employee_id = employee_id

    def __repr__(self) -> str:
        return "Role :: {self.name},  type :: {self.type}"
