from app.main.business_models.base_buisness_model import BaseModel


class Label(BaseModel):
    def __init__(self, name, color, default):
        self.name = name
        self.color = color
        self.default = default

