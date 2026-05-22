# all of the things here are type anotations and not variables
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # if the user dosent provide a value it default prints True


class PostCreate(PostBase):
    pass


class UserOUt(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOUt

    class congif:
        orm_mode = True


class CreateUser(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
