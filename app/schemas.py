from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field, EmailStr
from pydantic.generics import GenericModel

T = TypeVar('T')


class PostSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = False

    class Config:
        orm_mode = True


class RequestPost(BaseModel):
    parameter: PostSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    total: Optional[int]
    page: Optional[int]
    size: Optional[int]
    result: Optional[T]


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)
