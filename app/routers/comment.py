from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenData
from app.comment.schemas import CreateComment, ResponseComment
from app.utils import get_session
from fastapi import Depends, status, APIRouter

from app.oauth2 import get_current_user
from app.comment.crud import create_comment, user_update_comment

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: CreateComment, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    await create_comment(session, request.parameter, get_current_user_id.id)
    return ResponseComment(code=201, status="Ok", message="Comment successfully").dict(exclude_none=True)


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update_comment(request: CreateComment, session: AsyncSession = Depends(get_session),
                         get_current_user_id: TokenData = Depends(get_current_user)):
    comment = await user_update_comment(session, request.parameter, get_current_user_id.id)
    return ResponseComment(status="Ok", message=f"This is the post with id = {comment.id} after update",
                           result=comment)
