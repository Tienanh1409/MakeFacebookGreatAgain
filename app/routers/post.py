from app.utils import get_db
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from app.schemas import (
    RequestPost,
    Response
)
from app.oauth2 import get_current_user
from app import crud

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: RequestPost, db: Session = Depends(get_db),
                 get_current_user_id: int = Depends(get_current_user)):
    crud.create_post(db, request.parameter)
    return Response(code=201, status="Ok", message="Book created successfully").dict(exclude_none=True)


@router.get('/posts', status_code=status.HTTP_200_OK)
async def get_posts(page: int, size: int, db: Session = Depends(get_db)):
    posts, total = crud.get_posts(page, size, db)
    return Response(code=200, status="Ok", message="This is all posts", total=total, page=page, size=size, result=posts)


@router.get('/{id}', status_code=status.HTTP_201_CREATED)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot found post with id {id}")
    return Response(code=201, status="Ok", message=f"This is the post with id = {id}", result=post)


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update_post(request: RequestPost, db: Session = Depends(get_db)):
    post = crud.update_post(db, request.parameter.id, request.parameter.title, request.parameter.body)
    return Response(code=200, status="Ok", message=f"This is the post with id = {post.id} after update", result=post)


@router.delete('/delete/{id}')
async def delete_post(id: int, db: Session = Depends(get_db)):
    crud.remove_post(db, id)
    return Response(code=200, status="Ok", message=f"The post with id = {id} have been remove successfully")
