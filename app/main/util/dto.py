from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', 'User Related Operations')
    user = api.model('user', {
        'id': fields.Integer(required=False, description='Field is auto-generated'),
        'email': fields.String(required=True, description='User\'s email address'),
        'first_name': fields.String(required=True, description='User\'s first name'),
        'last_name': fields.String(required=True, description='User\'s last name'),
        'password': fields.String(required=True, description='User\'s password'),
        'username': fields.String(required=True, description='User\'s username'),
        'is_admin': fields.Boolean(required=False, description='Specify if user is admin', default=False),
        'gender': fields.String(required=True, description='User\'s gender male, female or unknown'),
        'user_avatar': fields.String(required=True, description='User\'s avatar link')
    })


class AuthDto:
    api = Namespace('auth', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'email_or_username': fields.String(required=True, description='The email address or user\'s username'),
        'password': fields.String(required=True, description='The user password '),
    })


class PostDto:
    api = Namespace('post', description='Post Related Operations')
    post = api.model('post_post', {
        'id': fields.Integer(required=False, description='Don\'t put anything here when sending'),
        'title': fields.String(required=True, description='Title od the post'),
        'content': fields.String(required=True, description='Post content'),
        'post_image': fields.String(required=True, description='Post image'),
        'user_id': fields.Integer(required=True, description='Id of user posting'),
        'no_of_likes': fields.Integer(required=False,
                                      description='No of likes the post have, leave blank when sending data')
    })

    post_with_user_detail = api.model('get_post', {
        'username': fields.String(required=False, descripiton='Users username'),
        'user_avatar': fields.String(required=False, description='Users avatar'),
        'user_email': fields.String(required=False, description='Users email address'),
        'id': fields.Integer(required=False, description='Don\'t put anything here when sending'),
        'title': fields.String(required=True, description='Title od the post'),
        'content': fields.String(required=True, description='Post content'),
        'post_image': fields.String(required=True, description='Post image'),
        'user_id': fields.Integer(required=True, description='Id of user posting'),
        'no_of_likes': fields.Integer(required=False,
                                      description='No of likes the post have, leave blank when sending data')
    })


class CommentDto:
    api = Namespace('comment', description='Comment Related Operations')
    comment = api.model('comment', {
        'id': fields.Integer(required=False, description='Don\'t put anything here when sending'),
        'comment': fields.String(required=True, description='The Comment'),
        'user_id': fields.Integer(required=True, description='Id of user commenting'),
        'post_id': fields.Integer(requird=True, description='Post being commented on')
    })
