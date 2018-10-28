from app.main.model.models import Gender
from ..service.user_service import *
from ..util.dto import UserDto
from flask_restplus import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

user_api = UserDto.api
_user = UserDto.user


@user_api.route('/')
class UserData(Resource):
    @user_api.doc('list of all registered users')
    @user_api.marshal_list_with(_user, envelope='data')
    @user_api.doc(params={'username': 'username', 'page': 'page requested'})
    def get(self):
        username = request.args.get('username')
        page = request.args.get('page')
        if not page:
            page = 1
        if not username:
            return get_all_users(int(page))
        else:
            return search_users_username(username, int(page))

    @user_api.response(201, 'user successfully created')
    @user_api.doc('create a new user')
    @user_api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return save_new_user(data=data)


@user_api.route('/<username>')
@user_api.param('username', 'The User\'s unique identifier')
@user_api.response(404, 'User not found.')
class SingleUserOperation(Resource):
    @user_api.doc('get a user')
    @user_api.marshal_with(_user)
    def get(self, username):
        user = get_a_user_username(username=username)
        if not user:
            user_api.abort(404)
        else:
            return user
