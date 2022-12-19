"""
123
"""
from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def read_root():
    """ asdasd """
    return {"Hello" : "Tien Anh ne"}

@app.get("/posts")
async def get_posts():
    """ get all the posts"""
    return {"data": " This is all of your posts"}


@app.post("/createpost")
async def create_a_post(payload: dict = Body(...)):
    """ Hello"""
    return {"message" : "Create a post successfully", "title" : payload.get("title") , "body" : payload.get("body")}