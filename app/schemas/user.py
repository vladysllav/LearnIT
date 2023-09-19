from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserType


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    is_active: Optional[bool] = Field(True, example=True)
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    type: Optional[UserType] = UserType.student
    date_of_birth: Optional[date] = Field(None, example="2000-01-01")
    phone_number: Optional[str] = Field(None, example="+380123456789")

    class Config:
        use_enum_values = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., example="securepassword")


class UserLogin(BaseModel):
    username: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, example="newsecurepassword")


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
