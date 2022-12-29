from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class CommentSchema(BaseModel):
    id: Optional[int] = None
    text: str
    comment_parent_id: Optional[int] = None
    post_id: Optional[int] = None

    class Config:
        orm_mode = True


class CreateComment(BaseModel):
    parameter: CommentSchema = Field(...)


class ResponseComment(GenericModel, Generic[T]):
    status: str
    message: str
    total: Optional[int]
    result: Optional[T]
