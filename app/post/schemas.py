from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class PostSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = False

    class Config:
        orm_mode = True


class CreatePost(BaseModel):
    parameter: PostSchema = Field(...)


class ResponsePost(GenericModel, Generic[T]):
    status: str
    message: str
    total: Optional[int]
    page: Optional[int]
    size: Optional[int]
    result: Optional[T]
