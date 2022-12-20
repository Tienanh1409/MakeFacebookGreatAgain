from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import Post
from .schemas import PostSchema

def get_posts(page:int, size:int, db:Session):
    posts = db.query(Post, func.count('id').over().label('total_post')).limit(size).offset(page*size).all()
    total = 0
    if posts:
        total = posts[0].total_post
    return posts , total

def get_post_by_id(db:Session, post_id:int):
    return db.query(Post).filter(Post.id==post_id).first()

def create_post(db:Session, post: PostSchema):
    _post = Post(title = post.title, body = post.body, published = post.published)
    db.add(_post)
    db.commit()
    db.refresh(_post)
    return _post

def remove_post(db:Session, post_id:int):
    _post = get_post_by_id(db, post_id)
    db.delete(_post)
    db.commit()

def update_post(db:Session, post_id:int, post_title: str, post_body:str):
    _post = get_post_by_id(db, post_id)
    _post.title = post_title
    _post.body = post_body
    db.commit()
    db.refresh(_post)
    return _post
