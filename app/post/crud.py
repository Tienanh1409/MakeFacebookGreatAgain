from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.model import (
    Post
)
from fastapi import HTTPException, status
from app.post.schemas import PostSchema


async def get_posts(page: int, size: int, session: AsyncSession):
    total = 0
    stmt = select(Post).add_columns(func.count().over().label('total')).order_by(Post.id)
    if size:
        stmt = stmt.limit(size)
    if page:
        stmt = stmt.offset(page * size)
    result = await session.execute(stmt)
    posts = result.fetchall()
    if posts:
        total = getattr(posts[0], "total", 0)
    return posts, total


async def get_post_by_id(post_id: int, session: AsyncSession):
    stmt = select(Post).where(Post.id == post_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def create_post(session: AsyncSession, post: PostSchema, owner_post_id: int):
    _post = Post(title=post.title, body=post.body, published=post.published, user_id=owner_post_id)
    session.add(_post)
    await session.commit()
    await session.refresh(_post)
    return _post


async def delete_post(session: AsyncSession, post_id: int, user_id: int):
    _post = await get_post_by_id(post_id, session)
    if not _post or _post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    await session.delete(_post)
    await session.commit()
    return True


async def user_update_post(session: AsyncSession, post: PostSchema, user_id: int):
    _post = await get_post_by_id(post.id, session)
    if user_id != _post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    _post.title = post.title
    _post.body = post.body
    await session.commit()
    await session.refresh(_post)
    return _post


async def get_posts_by_user_id(session: AsyncSession, user_id: int):
    stmt = select(Post).where(Post.user_id == user_id)
    result = await session.execute(stmt)
    return result.fetchall()
