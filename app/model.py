from sqlalchemy import Column, Integer, String, Boolean
from .config import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key = True)
    title = Column(String)
    body = Column(String)
    published = Column(Boolean, default = False)

    

    