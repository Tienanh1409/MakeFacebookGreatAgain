from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crud import user_login
from app.utils import get_session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    token = await user_login(request, session)
    return token
