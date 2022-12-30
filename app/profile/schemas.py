import datetime
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class ProfileSchema(BaseModel):
    name: Optional[str]
    address: Optional[str]
    avatar: Optional[str]
    school: Optional[str]
    age: Optional[int]
    gender_id: Optional[int]
    date_of_birth: Optional[datetime.date]

    class Config:
        orm_mode = True


class RequestProfile(BaseModel):
    parameter: ProfileSchema = Field(...)


class ResponseUser(GenericModel, Generic[T]):
    result: Optional[T]


class ProfileResponse(BaseModel):
    name: str
    address: Optional[str]
    avatar: Optional[str]
    school: Optional[str]
    age: Optional[int]
    date_of_birth: Optional[datetime.date]
