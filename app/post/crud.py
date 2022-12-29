from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.model import (
    Post
)
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
    return result.scalar_one_or_none()


async def create_post(session: AsyncSession, post: PostSchema, owner_post_id: int):
    _post = Post(title=post.title, body=post.body, published=post.published, user_id=owner_post_id)
    session.add(_post)
    await session.commit()
    await session.refresh(_post)
    return _post


async def remove_post(session: AsyncSession, post_id: int):
    _post = get_post_by_id(post_id, session)
    await session.delete(_post)
    await session.commit()
    return True


async def user_update_post(session: AsyncSession, post_id: int, post_title: str, post_body: str):
    _post = await get_post_by_id(post_id, session)
    _post.title = post_title
    _post.body = post_body
    await session.commit()
    await session.refresh(_post)
    return _post
