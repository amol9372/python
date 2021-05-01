from flask_restx import Api
from flask import Blueprint
from .main.controller.user_resource import api as user_api
from .main.controller.task_resource import api as task_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_api, path='/user/')
api.add_namespace(task_api, path='/resource/')