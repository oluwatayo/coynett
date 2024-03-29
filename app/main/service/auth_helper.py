from app.main.model.models import User
from ..service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email_or_username')).first()
            if not user:
                user = User.query.filter_by(username=data.get('email_or_username')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.public_id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email/username or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request, token = None):
        # get the auth token
        if new_request is not None:
            auth_token = new_request.headers.get('Authorization')
        else:
            auth_token = token
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                print(resp)
                user = User.query.filter_by(public_id=resp).first()
                if not user:
                    response_object = {
                        'status': 'fail',
                        'message': resp
                    }
                    return response_object, 401

                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'public_id': user.public_id,
                        'email': user.email,
                        'admin': user.is_admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
