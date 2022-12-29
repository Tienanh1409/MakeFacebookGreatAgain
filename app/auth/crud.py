from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.crud import get_user_by_username
from app.oauth2 import create_access_token

from fastapi import HTTPException, status
from app.utils import verify


async def user_login(user_input: OAuth2PasswordRequestForm, session: AsyncSession):
    user = await get_user_by_username(user_input.username, session)
    if not user or not verify(user_input.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The email and/or password you specified are not correct.")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

