from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    profile = relationship("Profile", uselist=False, back_populates="user")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    published = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)


class Gender(Base):
    __tablename__ = 'genders'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    label = Column(String, nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    school = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    date_of_birth = Column(Date)

    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="profile")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.now)
