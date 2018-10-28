from functools import wraps
from ..service.auth_helper import Auth
from flask import request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user_data = data.get('data')

        if not user_data:
            return data, status

        return f(*args, user_data, **kwargs)

    return decorated
