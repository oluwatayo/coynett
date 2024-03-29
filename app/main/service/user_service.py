import uuid
import datetime
from sqlalchemy.exc import IntegrityError
from app.main import db
from app.main.model.models import User


def generate_token(user):
    try:
        auth_token = User.encode_auth_token(user.public_id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_new_user(data):
    try:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            user_avatar=data['user_avatar'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()
        response_object = generate_token(new_user)
    except IntegrityError as e:
        print(e)
        response_object = {
                              'status': 'error',
                              'message': 'Email or Username Already Exists. Login Instead'
                          }, 409
    return response_object


def get_all_users(page):
    users = User.query.paginate(page=page)
    return users.items


def get_a_user_public_id(public_id):
    return User.query.filter_by(public_id=public_id).first()


def get_a_user_email(email):
    return User.query.filter_by(email=email).first()


def get_a_user_username(username):
    return User.query.filter_by(username=username).first()


def search_users_username(username, page):
    users = User.query.filter(User.username.contains(username)).paginate(page=page)
    return users.items


def update_a_user(public_id, data):
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.gender = data['gender']
        user.user_avatar = data['avatar']

        db.session.commit()
        response_object = {"status": "successful", "message": "user data updated"}
        response_code = 201
    else:
        response_object = {"status": "error", "message": "user does not exist"}
        response_code = 409

    return response_object, response_code


def delete_a_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        response_object = {"status": "successful", "message": "user deleted"}
        response_code = 201
    else:
        response_object = {"status": "error", "message": "user to be deleted not found"}
        response_code = 409

    return response_object, response_code
