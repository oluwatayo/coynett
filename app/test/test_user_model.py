import unittest
import datetime
import uuid

from app.main import db
from app.main.model.models import User, Gender
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            public_id=str(uuid.uuid4()),
            email='test@email.com',
            first_name='first_name',
            last_name='last_name',
            gender=Gender.Male,
            username='username',
            password='password',
            registered_on=datetime.datetime.utcnow())

        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            public_id=str(uuid.uuid4()),
            email='test@email.com',
            first_name='first_name',
            last_name='last_name',
            gender=Gender.Male,
            username='username',
            password='password',
            registered_on=datetime.datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)

        if __name__ == '__main__':
            unittest.main()
