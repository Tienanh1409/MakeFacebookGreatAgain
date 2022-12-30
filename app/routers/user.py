from sqlalchemy.ext.asyncio import AsyncSession

from app.post.schemas import ResponsePost
from app.user.schemas import RequestUser
from app.utils import get_session
from fastapi import Depends, status, APIRouter

from app.user.crud import get_users, create_user

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: RequestUser, session: AsyncSession = Depends(get_session)):
    await create_user(session, request.parameter)
    return ResponsePost(code=201, status="Ok", message="user created successfully").dict(exclude_none=True)


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_all(session: AsyncSession = Depends(get_session)):
    users = await get_users(session)
    return ResponsePost(code=200, status="Ok", message="This all the user", result=users)

