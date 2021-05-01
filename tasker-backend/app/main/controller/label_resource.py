from flask_jwt import jwt_required
from flask_restx import Resource, api

from app.main.db_models.task.labels import UserLabel
from app.main.db_models.task.sections import Section

from app.main.db_models.task.tasks import Task
from ..util import ResourceDto

api = ResourceDto.api



@api.route("label")
class Labels(Resource):

    #   { "name" : "" , user_id : context, "color" : ""  }   

    @jwt_required()
    def post(self):
           
        pass
    
    def get(self):
        pass

    def delete(self):
        pass  