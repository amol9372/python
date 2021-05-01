from app.main.business_models.base_buisness_model import BaseModel


class Task(BaseModel):
    
    def __init__(self, name, description, priority, status, schedule):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.schedule = schedule