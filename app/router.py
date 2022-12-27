from fastapi import APIRouter, HTTPException, Depends, status
from app.config import SessionLocal
from sqlalchemy.orm import Session
from app.schemas import RequestPost, Response, RequestUser
from app import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create/post', status_code=status.HTTP_201_CREATED)
async def create(request: RequestPost, db: Session = Depends(get_db)):
    crud.create_post(db, request.parameter)
    return Response(code=201, status="Ok", message="Book created successfully").dict(exclude_none=True)


@router.get('/posts/')
async def get_posts(page: int, size: int, db: Session = Depends(get_db)):
    posts, total = crud.get_posts(page, size, db)
    return Response(code=200, status="Ok", message="This is all posts", total=total, page=page, size=size, result=posts)


@router.get('/post/{id}', status_code=status.HTTP_201_CREATED)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot found post with id {id}")
    return Response(code=201, status="Ok", message=f"This is the post with id = {id}", result=post)


@router.patch('/update')
async def update_post(request: RequestPost, db: Session = Depends(get_db)):
    post = crud.update_post(db, request.parameter.id, request.parameter.title, request.parameter.body)
    return Response(code=200, status="Ok", message=f"This is the post with id = {post.id} after update", result=post)


@router.delete('/delete/{id}')
async def delete_post(id: int, db: Session = Depends(get_db)):
    crud.remove_post(db, id)
    return Response(code=200, status="Ok", message=f"The post with id = {id} have been remove successfully")


@router.post('/create/user', status_code=status.HTTP_201_CREATED)
async def create_user(request: RequestUser, db: Session = Depends(get_db)):
    crud.create_user(db, request.parameter)
    return Response(code=201, status="Ok", message="user created successfully").dict(exclude_none=True)


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return Response(code=200, status="Ok", message="This all the user", result=users)
