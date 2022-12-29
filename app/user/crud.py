from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import (
    User
)

from fastapi import HTTPException, status

from app.user.schemas import UserSchema
from app.utils import hash_password


async def create_user(session: AsyncSession, user: UserSchema):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The passwords you entered do not match.")
    hashed_password = hash_password(user.password)
    _user = User(email=user.email, password=hashed_password, username=user.username, gender_id=user.gender_id)
    session.add(_user)
    await session.commit()
    await session.refresh(_user)
    return _user


async def get_users(session: AsyncSession):
    stmt = select(User)
    users = await session.execute(stmt)
    return users.fetchall()


async def get_user_by_username(username: str, session: AsyncSession):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
