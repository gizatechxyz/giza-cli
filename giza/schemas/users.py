from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, validator


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: SecretStr

    @validator("username", "email", "password")
    def str_not_emtpy(cls, s: str):
        if s == "":
            raise ValueError
        return s


class UserLogin(BaseModel):
    username: str
    password: SecretStr


class UserResponse(UserBase):
    username: str
    email: EmailStr
    is_active: bool
