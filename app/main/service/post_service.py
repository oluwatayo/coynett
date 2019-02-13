from ..model.models import Post, PostUserLikes, Comment, User
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


def get_post(page):
    posts = Post.query.paginate(page=page)
    return posts.items


'''def get_post_with_user_det(page):
    #posts = Post.query.join(User, Post.user_id==User.id).first()
    #print(posts.user.public_id)
    posts = Post.query.filter_by(id=3).first()
    posts.public_id = posts.user.public_id
    print(posts.user.public_id)
    #posts = Post.query.paginate(page=page)
    return posts'''


def get_post_with_user_det(page):
    # posts = db.session.query(Post, User.public_id).filter(Post.user_id==User.id).first()
    # posts = Post.query.join(User, Post.user_id==User.id).add_columns(Post.user).first()
    # print(posts.statement)
    # posts = Post.query.paginate(page=page)
    '''posts = Post.query.join(User, Post.user_id == User.id).add_columns(User.public_id, Post.id, Post.user_id,
                                                                       Post.post_image, Post.content,
                                                                       Post.no_of_likes).all()'''

    posts = Post.query.join(User, Post.user_id == User.id).paginate(page=page)
    posts = [Post.set_user(post) for post in posts.items]
    print(posts)
    return posts


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


def like_post(post_id, data):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': 'error', 'message': 'Post does not exist'}, 400

    post.no_of_likes = post.no_of_likes + 1
    liked_post = PostUserLikes(user_id=data['user_id'], post_id=post_id)
    db.session.add(liked_post)
    db.session.commit()
    return {'status': 'success', 'message': 'post liked'}, 200


def unlike_post(post_id, data):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return {'status': 'error', 'message': 'Post does not exist'}, 400

    if post.no_of_likes >= 1:
        post.no_of_likes = post.no_of_likes - 1

    post_liked = PostUserLikes.query.filter_by(post_id=post_id, user_id=data['user_id']).first()
    if not post_liked:
        return {'status': 'error', 'message': 'User hasn\'t liked post'}, 400

    db.session.delete(post_liked)
    db.session.commit()
    return {'status': 'success', 'message': 'post unliked'}, 200


def create_comment(comment_data):
    if not comment_data:
        response_object = {
                              'status': 'error',
                              'message': 'no comment data'
                          }, 400
        return response_object
    comment = Comment(comment=comment_data['comment'],
                      post_id=comment_data['post_id'],
                      user_id=comment_data['user_id'])

    try:
        db.session.add(comment)
        db.session.commit()
        return {'status': 'success', 'message': 'user commented'}, 201
    except Exception as e:
        print(e)
        response_object = {
                              'status': 'error',
                              'message': e
                          }, 400
        return response_object


def get_post_comments(post_id, page):
    comments = Comment.query.filter_by(post_id=post_id).paginate(page=page)
    return comments.items, 200


def delete_all_post_comment(data, post_id):
    if not data['admin']:
        return {'status': 'error', 'message': 'only admins can delete all comments'}, 400
    comments = Comment.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    return {'status': 'success', 'message': str(comments) + ' comment(s) deleted'}, 200


def delete_comment(comment_id, user_data):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return {'status': 'error', 'message': 'comment not found'}, 404
    if comment.user_id != user_data['user_id'] and not user_data['admin']:
        return {'status': 'error', 'message': 'user is not authorized to delete this comment'}, 400
    db.session.delete(comment)
    db.session.commit()
    return {'status': 'success', 'message': 'comment deleted'}, 200
