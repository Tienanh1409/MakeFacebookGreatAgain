from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenData
from app.post.schemas import CreatePost, ResponsePost
from app.utils import get_session
from fastapi import HTTPException, Depends, status, APIRouter
from app.oauth2 import get_current_user
from app.post.crud import (
    create_post,
    get_posts,
    get_post_by_id,
    user_update_post,
    remove_post
)

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(request: CreatePost, session: AsyncSession = Depends(get_session),
                 get_current_user_id: TokenData = Depends(get_current_user)):
    await create_post(session, request.parameter, get_current_user_id.id)
    return ResponsePost(status="Ok", message="Post created successfully").dict(exclude_none=True)


@router.get('/posts', status_code=status.HTTP_200_OK)
async def get_posts(page: int, size: int, session: AsyncSession = Depends(get_session)):
    posts, total = await get_posts(page, size, session)
    return ResponsePost(status="Ok", message="This is all posts", total=total, page=page, size=size,
                        result=posts)


@router.get('/{post_id}', status_code=status.HTTP_201_CREATED)
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await get_post_by_id(post_id, session)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot found post with id {post_id}")
    return ResponsePost(status="Ok", message=f"This is the post with id = {post_id}", result=post)


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update_post(request: CreatePost, session: AsyncSession = Depends(get_session)):
    post = await user_update_post(session, request.parameter.id, request.parameter.title, request.parameter.body)
    return ResponsePost(status="Ok", message=f"This is the post with id = {post.id} after update",
                        result=post)


@router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
    await remove_post(session, post_id)
    return ResponsePost(status="Ok", message=f"The post with id = {post_id} have been remove successfully")
