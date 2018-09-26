from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import user_api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Coynett API Documentation',
          version='1.0',
          description='a documentation for coynett flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')