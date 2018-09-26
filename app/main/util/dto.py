from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', 'User Related Operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='User\'s email address'),
        'first_name': fields.String(required=True, description='User\'s first name'),
        'last_name': fields.String(required=True, description='User\'s last name'),
        'password': fields.String(required=True, description='User\'s password'),
        'username': fields.String(required=True, description='User\'s username'),
        'gender': fields.String(required=True, description='User\'s gender male, female or unknown'),
        'user_avatar': fields.String(required=True, description='User\'s avatar link')
    })
