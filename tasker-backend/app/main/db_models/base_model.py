import datetime
from app.main import db

class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    created_on = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.now())
