from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app import crud
from app.utils import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login(db, request)
