from ..util.dto import PostDto, CommentDto
from ..util.decorator import token_required
from ..service.post_service import *
from flask_restplus import Resource
from flask import request

api = PostDto.api
a_post = PostDto.post
c_api = CommentDto.api
a_comment = CommentDto.comment


@api.route('/')
class Post(Resource):
    @api.doc(params={'page': 'page being requested'})
    @api.marshal_list_with(a_post, envelope='data')
    def get(self):
        page = request.args.get('page')
        if not page:
            page = 1
        return get_post(int(page))

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


@api.route('/like/<post_id>')
class LikePost(Resource):
    @token_required
    def post(self, data, post_id):
        return like_post(post_id, data)


@api.route('/unlike/<post_id>')
class UnlikePost(Resource):
    @token_required
    def post(self, data, post_id):
        return unlike_post(post_id, data)


@c_api.route('/<post_id>')
class PostComment(Resource):
    @api.expect(a_comment)
    def post(self):
        data = request.json
        return create_comment(data)

    @c_api.marshal_list_with(a_comment, envelope='data')
    @c_api.doc(params={'page': 'requested page'})
    def get(self, post_id):
        page = request.args.get('page')
        if not page:
            page = 1
        return get_post_comments(post_id,int(page))

    @token_required
    def delete(self, data, post_id):
        return delete_all_post_comment(data, post_id)



@c_api.route('/c/<comment_id>')
@c_api.response(404, 'Comment not found')
class PostSingleComment(Resource):
    @token_required
    def delete(self, data, comment_id):
        return delete_comment(comment_id, data)


    @c_api.doc('get a comment by its ID')
    @c_api.marshal_with(a_comment)
    def get(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            c_api.abort(404)
        return comment
