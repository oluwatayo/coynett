from ..model.models import Post
from .. import db


def create_post(post_data):
    if not post_data:
        response_object = {
                              'status': 'error',
                              'message': 'no post data'
                          }, 400
        return response_object
    post = Post(title=post_data['title'],
                content=post_data['content'],
                post_image=post_data['post_image'],
                user_id=post_data['user_id'])

    try:
        db.session.add(post)
        db.session.commit()
        return {'status': 'success', 'message': 'post created'}, 201
    except Exception as e:
        print(e)
        response_object = {
                              'status': 'error',
                              'message': e
                          }, 400
        return response_object


def get_post(start):
    return Post.query.filter(Post.id >= start).all()


def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': 'error', 'message': 'post does not exist'}, 400
    try:
        db.session.delete(post)
        db.session.commit()
        return {'status': 'success', 'message': 'Post was successfully deleted'}, 200
    except Exception as e:
        return {'status': 'error', 'message': e}, 400


def update_post(post_id, post_data):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': 'error', 'message': 'post does not exist'}, 400
    post.title = post_data['title']
    post.content = post_data['content']
    post.post_image = post_data['post_image']
    db.session.commit()
    return {'status': 'success', 'message': 'post updated'}, 200
