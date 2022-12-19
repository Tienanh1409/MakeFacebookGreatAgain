"""
123
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    """ asdasd """
    return {"Hello" : "Tien Anh ne"}

@app.get("/posts")
async def get_posts():
    """ get all the posts"""
    return {"data": " This is all of your posts"}
