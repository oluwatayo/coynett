from .. import db, flask_bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import enum


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


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='posts', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return "Post Title: {}".format(self.title)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(50), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "Comment {}".format(self.id)
