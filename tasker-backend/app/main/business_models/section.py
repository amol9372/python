from app.main.business_models.base_buisness_model import BaseModel


class Section(BaseModel):

    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
