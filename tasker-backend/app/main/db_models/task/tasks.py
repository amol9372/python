from grpc import Status
from app.main import db
from app.main.db_models.base_model import BaseModel

class Task(BaseModel):

    __tablename__ = "tasks"

    name = db.Column(db.Text)
    description = db.Column(db.Text)
    # Foreign key column
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    priority_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    status = db.Column(db.Text)
    schedule = db.Column(db.Text)
    

    def __init__(self, name, description, section_id, priority_id, schedule = None,status="active"):
        self.name = name
        self.description = description
        self.section_id = section_id
        self.status = status
        self.priority_id = priority_id
        self.schedule = schedule

    @staticmethod
    def createTask(task):
        db.session.add(task)
        db.session.commit()

    @staticmethod
    def get_tasks_for_section(section_id):
        return Task.query.filter_by(section_id).all()  
 
    def __repr__(self) -> str:
        return "Task with name ::: {} and section ::: {} and status ::: {}".format(self.name, self.section_id, self.status)    

    
