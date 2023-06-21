from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    username: str
    email: str
    password: str


class User(UserBase):
    pass
