from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.comment.schemas import CommentSchema
from app.model import Comment


async def create_comment(session: AsyncSession, comment: CommentSchema, user_id: int):
    _comment = Comment(text=comment.text, post_id=comment.post_id, user_id=user_id)
    if comment.comment_parent_id:
        _post = await get_comment_by_id(session, comment.comment_parent_id)
        _comment = Comment(text=comment.text, post_id=_post.id, user_id=user_id,
                           comment_parent_id=comment.comment_parent_id)
    session.add(_comment)
    await session.commit()
    await session.refresh(_comment)
    return _comment


async def user_update_comment(session: AsyncSession, comment: CommentSchema, user_id: int):
    _comment = await get_comment_by_id(session, comment.id)
    if _comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied")
    _comment.text = comment.text
    await session.commit()
    await session.refresh(_comment)
    return _comment


async def get_comment_by_id(session: AsyncSession, comment_id: int):
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    return result.fetchone()


async def delete_comment(session: AsyncSession, comment_id: int, user_id: int):
    _comment = await get_comment_by_id(session, comment_id)
    if _comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied")
    await session.delete(_comment)
    await session.commit()
    return True


async def get_comments_by_post_id(session: AsyncSession, post_id: int):
    stmt = select(Comment).where(Comment.post_id == post_id)
    result = await session.execute(stmt)
    return result.fetchall()

