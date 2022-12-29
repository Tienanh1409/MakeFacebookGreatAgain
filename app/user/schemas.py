from pydantic import EmailStr
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class UserSchema(BaseModel):
    gender_id: Optional[int] = None
    email: EmailStr
    username: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    confirm_password: str = Field(min_length=6, max_length=20)

    class Config:
        orm_mode = True


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class ResponseUser(GenericModel, Generic[T]):
    result: Optional[T]
