import json
from app.test.base import BaseTestCase
from app.test.test_auth import register_user
from app.test.test_auth import login_user
from app.main.service.auth_helper import Auth
from app.main.service.post_service import create_post


def register_and_get_user_data(self):
    register_response = register_user(self)
    response_data = json.loads(register_response.data.decode())
    token = response_data['Authorization']
    user_data = Auth.get_logged_in_user(token)
    # print(user_data[0])
    return user_data[0].get('data')['user_id']


class PostTest(BaseTestCase):
    def test_create_post(self):
        with self.client:
            user_id = register_and_get_user_data(self)
            req = self.client.post('/api/v1/post/', data=json.dumps(dict(
                post_id=0,
                title='string',
                content='string',
                post_image='string',
                user_id=user_id
            )), content_type='application/json')
            response_data = json.loads(req.data.decode())
            self.assertTrue(req.status_code, 201)
            print(response_data)
            self.assertTrue(response_data.get('status'), 'success')

    def test_update_no_post(self):
        post_id = 1000
        with self.client:
            req = self.client.put('/api/v1/posts/' + str(post_id),
                                  data=json.dumps(dict(
                                      post_id=post_id,
                                      title='string',
                                      content='string',
                                      post_image='string'
                                  )), content_type='application/json')
            self.assertTrue(req.status_code, 404)
