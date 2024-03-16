from datetime import datetime

from typing import Optional, Union
from pydantic import Field
from pydantic import BaseModel


class BaseCourse(BaseModel):
    name: Optional[str] = Field(None, example='ULTIMATE Python course')
    description: Optional[str] = Field(None, example='The best Python course in the World!')
    is_active: Optional[bool] = Field(True, example=True)


class BaseCourseRating(BaseModel):
    value: Optional[int] = Field(None, example=4)


class CourseRead(BaseCourse):
    id: Optional[int] = Field(None, example=1)
    rating: Optional[float] = Field(None, example=4.7)
    created_at: Optional[datetime] = Field(None, example='2023-02-21')
    updated_at: Optional[datetime] = Field(None, example='2023-03-05')

    class Config:
        orm_mode = True


class CourseRatingRead(BaseCourseRating):
    id: Optional[int] = Field(None, example=1)
    user_id: Optional[int] = Field(None, example=1)
    course_id: Optional[int] = Field(None, example=1)
    created_at: Optional[datetime] = Field(None, example='2023-02-21')
    updated_at: Optional[datetime] = Field(None, example='2023-03-05')

    class Config:
        orm_mode = True


class CourseRatingCreate(BaseCourseRating):
    pass


class CourseCreate(BaseCourse):
    pass
    
       
class CourseUpdate(BaseCourse):
    pass
