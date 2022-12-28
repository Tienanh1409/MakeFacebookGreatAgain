from fastapi import FastAPI
from app.config import engine
from app import model
from app.routers import auth, post, user

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(router=post.router, prefix="/post", tags=["Post"])
app.include_router(router=user.router, prefix="/user", tags=["User"])
app.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
