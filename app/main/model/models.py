import enum
import datetime
import jwt
from .. import db, flask_bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import key


class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"
    Pnts = "Pnts"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(30), unique=True)
    gender = db.Column(db.Enum(Gender))
    user_avatar = db.Column(db.String(200),
                            default='https://cdn.pixabay.com/photo/2016/11/08/15/21/user-1808597_960_720.png')
    hashed_password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    posts = db.relationship('Post', backref='users', cascade='all, delete-orphan', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', cascade='all, delete-orphan', lazy='dynamic')
    posts_likes = db.relationship('PostUserLikes', backref='users', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password: write only field')

    @password.setter
    def password(self, password):
        self.hashed_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return "User {}".format(self.username)

    @staticmethod
    def encode_auth_token(public_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1, days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': public_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(200))
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    minute_read = db.Column(db.Integer, nullable=False, default=5)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    no_of_likes = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship('Comment', backref='posts', cascade='all, delete-orphan', lazy='dynamic')
    post_likes = db.relationship('PostUserLikes', backref='posts', cascade='all, delete-orphan', lazy='dynamic')
    user = db.relationship('User', backref='user_posts')

    def __repr__(self):
        return "Post Title: {}".format(self.title)

    @staticmethod
    def set_user(post):
        post.username = post.user.username
        post.user_email = post.user.email
        post.user_avatar = post.user.user_avatar
        return post


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(50), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "Comment {}".format(self.id)


class PostUserLikes(db.Model):
    __tablename__ = 'post_user_likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return "{}__{}".format(self.user_id, self.post_id)
