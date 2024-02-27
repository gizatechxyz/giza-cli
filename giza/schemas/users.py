from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: SecretStr

    @field_validator("username", "email", "password")
    @classmethod
    def str_not_emtpy(cls, s: str):
        """
        Validate that none of the provided information is an empty string

        Args:
            s (str): value to check if `""`

        Raises:
            ValueError: If the value is an empty string

        Returns:
            str: return the provided value if not empty
        """
        if s == "" or s is None:
            raise ValueError
        return s


class UserLogin(BaseModel):
    username: str
    password: SecretStr


class UserResponse(UserBase):
    username: str
    email: EmailStr
    is_active: bool


class UserCreateApiKeys(BaseModel):
    id: SecretStr
