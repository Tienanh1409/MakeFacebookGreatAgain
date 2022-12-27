from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.model import Post, User
from app.schemas import PostSchema, RequestUser


def get_posts(page: int, size: int, db: Session):
    total = 0
    stmt = select(Post).add_columns(func.count().over().label('total')).order_by(Post.id)
    if size:
        stmt = stmt.limit(size)
    if page:
        stmt = stmt.offset(page * size)
    posts = db.execute(stmt).all()
    if posts:
        total = getattr(posts[0], "total", 0)
    return posts, total


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post: PostSchema):
    _post = Post(title=post.title, body=post.body, published=post.published)
    db.add(_post)
    db.commit()
    db.refresh(_post)
    return _post


def remove_post(db: Session, post_id: int):
    _post = get_post_by_id(db, post_id)
    db.delete(_post)
    db.commit()


def update_post(db: Session, post_id: int, post_title: str, post_body: str):
    _post = get_post_by_id(db, post_id)
    _post.title = post_title
    _post.body = post_body
    db.commit()
    db.refresh(_post)
    return _post


def create_user(db: Session, user: RequestUser):
    _user = User(email=user.email, password=user.password)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def get_users(db: Session):
    stmt = select(User)
    users = db.execute(stmt).fetchall()
    return users
