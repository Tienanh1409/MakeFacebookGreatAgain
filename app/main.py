from fastapi import FastAPI
from app.routers import auth, post, user, comment, profile

app = FastAPI()

app.include_router(router=post.router, prefix="/post", tags=["Post"])
app.include_router(router=user.router, prefix="/user", tags=["User"])
app.include_router(router=auth.router, prefix="/auth", tags=["Auth"])
app.include_router(router=comment.router, prefix="/comment", tags=["Comment"])
app.include_router(router=profile.router, prefix="/profile", tags=["Profile"])
