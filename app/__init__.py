from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import user_api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.post_controller import api as post_ns, c_api as comment_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
auth = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(blueprint,
          authorizations=auth,
          doc='/docs',
          title='Coynett API Documentation',
          version='1.0',
          description='a documentation for coynett flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(post_ns)
api.add_namespace(comment_ns)
