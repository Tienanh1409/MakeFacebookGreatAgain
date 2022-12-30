from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.helper import update_model_field
from app.model import (
    Gender,
    Profile
)
from app.profile.schemas import ProfileSchema


async def get_gender_by_id(gender_id, session: AsyncSession):
    if not gender_id:
        return None
    stmt = select(Gender).where(Gender.id == gender_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_profile_by_user_id(user_id: int, session: AsyncSession) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one()


async def update_user_profile(request: ProfileSchema, user_id: int, session: AsyncSession):
    _profile = await get_profile_by_user_id(user_id, session)
    update_model_field(_profile, "name", request.name)
    update_model_field(_profile, "address", request.address)
    update_model_field(_profile, "avatar", request.avatar)
    update_model_field(_profile, "school", request.school)
    update_model_field(_profile, "age", request.age)
    update_model_field(_profile, "gender_id", request.gender_id)
    update_model_field(_profile, "date_of_birth", request.date_of_birth)
    await session.commit()
    await session.refresh(_profile)
    return _profile


async def create_user_profile(request: ProfileSchema, user_id: int, session: AsyncSession):
    _profile = Profile(name=request.name, address=request.address, avatar=request.avatar, school=request.school,
                       age=request.age, gender_id=request.gender_id, user_id=user_id,
                       date_of_birth=request.date_of_birth)
    session.add(_profile)
    await session.commit()
    await session.refresh(_profile)
    return _profile
