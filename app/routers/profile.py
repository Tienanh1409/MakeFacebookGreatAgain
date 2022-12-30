from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenData
from app.oauth2 import get_current_user
from app.profile.crud import create_user_profile, update_user_profile
from app.profile.schemas import RequestProfile, ProfileResponse
from app.utils import get_session
from fastapi import Depends, status, APIRouter

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: RequestProfile, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    profile = await create_user_profile(request.parameter, get_current_user_id.id, session)
    return profile


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(request: RequestProfile, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    _profile = await update_user_profile(request.parameter, get_current_user_id.id, session)
    return ProfileResponse(name=_profile.name, address=_profile.address, avatar=_profile.avatar, school=_profile.school,
                           age=_profile.age, date_of_birth=_profile.date_of_birth)
