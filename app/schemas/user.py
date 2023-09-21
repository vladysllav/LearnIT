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


# Properties to receive via API on creation
class UserCreate(UserBase):
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student
    password: str = Field(..., example="securepassword")


class UserLogin(BaseModel):
    username: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student
    password: Optional[str] = Field(None, example="newsecurepassword")


class UserInDBBase(UserBase):
    is_active: Optional[bool] = Field(True, example=True)
    type: Optional[UserType] = UserType.student
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
