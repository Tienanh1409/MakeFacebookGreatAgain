from app.utils import get_db
from fastapi import Depends, status, APIRouter

from sqlalchemy.orm import Session
from app.schemas import (
    Response,
    RequestUser
)
from app import crud

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(request: RequestUser, db: Session = Depends(get_db)):
    crud.create_user(db, request.parameter)
    return Response(code=201, status="Ok", message="user created successfully").dict(exclude_none=True)


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return Response(code=200, status="Ok", message="This all the user", result=users)
