from app.main import db

from app.main.db_models.base_model import BaseModel

class Priority(BaseModel):

    __tablename__ = "priority"
    
    name = db.Column(db.Text)
    description = db.Column(db.Text)


    def __init__(self, name, description) :
        self.name = name
        self.description = description
