from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.model import (
    Post,
    User
)
from app.oauth2 import create_access_token
from app.schemas import (
    PostSchema,
    UserSchema
)
from fastapi import HTTPException, status
from app.utils import hash_password, verify

""" ------------- POST -------------"""


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


""" ------------- USER -------------"""


def create_user(db: Session, user: UserSchema):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The passwords you entered do not match.")
    hashed_password = hash_password(user.password)
    _user = User(email=user.email, password=hashed_password, username=user.username)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def get_users(db: Session):
    stmt = select(User)
    users = db.execute(stmt).fetchall()
    return users


def get_user_by_username(db: Session, username: str):
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalar_one_or_none()
    return user


"""------------- AUTH -------------"""


def login(db: Session, user_input: OAuth2PasswordRequestForm):
    user = get_user_by_username(db, user_input.username)
    if not user or not verify(user_input.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The email and/or password you specified are not correct.")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
