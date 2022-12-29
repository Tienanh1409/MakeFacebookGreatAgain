from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model import (
    Gender
)


async def get_gender_by_id(gender_id, session: AsyncSession):
    if not gender_id:
        return None
    stmt = select(Gender).where(Gender.id == gender_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
