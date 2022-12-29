from typing import Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class UserLogin(BaseModel):
    username: str
    password: str


class RequestUserLogin(BaseModel):
    parameter: UserLogin = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
