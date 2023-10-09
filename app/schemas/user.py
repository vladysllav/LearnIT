from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserType


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    date_of_birth: Optional[date] = Field(None, example="2000-01-01")
    phone_number: Optional[str] = Field(None, example="+380123456789")


class UserSignUp(UserBase):
    password: str = Field(..., example="securepassword")


class UserCreate(UserBase):
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student
    password: str = Field(..., example="securepassword")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student


class User(UserBase):
    id: Optional[int] = None
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student

    class Config:
        orm_mode = True
