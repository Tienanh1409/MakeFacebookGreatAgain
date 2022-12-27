"""
123
"""
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from app.config import engine
from app import model
from app.router import router

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    body: str
    published: bool = True
    rating: Optional[int] = None


app.include_router(router=router, prefix="/post", tags=["post"])
