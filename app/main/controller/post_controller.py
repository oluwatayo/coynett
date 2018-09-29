from ..util.dto import PostDto
from ..service.post_service import *
from flask_restplus import Resource
from flask import request

api = PostDto.api
a_post = PostDto.post


@api.route('/')
class Post(Resource):
    @api.doc(params={'start': 'where to start from'})
    @api.marshal_list_with(a_post, envelope='data')
    def get(self):
        start = request.args.get('start')
        if not start:
            start = 1
        return get_post(start)

    @api.expect(a_post)
    def post(self):
        post_data = request.json
        return create_post(post_data=post_data)


@api.route('/<post_id>')
class PostWithId(Resource):
    @api.expect(a_post)
    def put(self, post_id):
        post_data = request.json
        return update_post(post_id=post_id, post_data=post_data)

    def delete(self, post_id):
        return delete_post(post_id=post_id)
