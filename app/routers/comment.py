from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenData
from app.comment.schemas import CreateComment, ResponseComment
from app.utils import get_session
from fastapi import Depends, status, APIRouter

from app.oauth2 import get_current_user
from app.comment.crud import create_comment, user_update_comment, delete_comment, get_comments_by_post_id

router = APIRouter()


@router.get('/{post_id}', status_code=status.HTTP_200_OK)
async def get_comments_of_post(post_id: int, session: AsyncSession = Depends(get_session)):
    comments = await get_comments_by_post_id(session, post_id)
    return comments


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: CreateComment, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    await create_comment(session, request.parameter, get_current_user_id.id)
    return ResponseComment(code=201, status="Ok", message="Comment successfully").dict(exclude_none=True)


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(request: CreateComment, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    comment = await user_update_comment(session, request.parameter, get_current_user_id.id)
    return ResponseComment(status="Ok", message=f"This is the post with id = {comment.id} after update",
                           result=comment)


@router.delete('/delete/{comment_id}', status_code=status.HTTP_200_OK)
async def delete(comment_id: int, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    return delete_comment(session, comment_id, get_current_user_id.id)
