"""
123
"""
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .config import engine
from . import model
from .router import router

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    body: str
    published: bool = True
    rating: Optional[int] = None

app.include_router(router=router, prefix="/post", tags=["post"])