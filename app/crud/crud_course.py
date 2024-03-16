from typing import Union, Dict, Any
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.course import CourseCreate, CourseUpdate, CourseRatingCreate
from app.models.course import Course, CourseRating
from app.crud.base import CRUDBase
from app.crud.crud_user import user
from app.models.user import User


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    def create(self, db: Session, *, obj_in: CourseCreate,
                current_user: User) -> Course:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")
        
        course_data = obj_in.dict()
        course_data['created_by_id'] = current_user.id
        course_data['created_at'] = datetime.utcnow()
        
        db_obj = Course(**course_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Course,
               obj_in: Union[CourseUpdate, Dict[str, Any]]) -> Course:
            
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


class CRUDCourseRating(CRUDBase[CourseRating, CourseRatingCreate, None]):
    def get(self, db: Session, *, user_id: int, course_id: int) -> CourseRating:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.course_id == course_id
        ).first()

    def create(
            self,
            db: Session,
            *,
            user_id: int,
            course_id: int,
            value: int
    ) -> CourseRating:

        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if not (1 <= value <= 5):
            raise HTTPException(status_code=400, detail="Invalid rating. Must be between 1 and 5.")

        existing_rating = self.get(db=db, user_id=user_id, course_id=course_id)
        if existing_rating:
            raise HTTPException(status_code=400, detail="You have already rated this course.")

        db_obj = self.model(user_id=user_id, course_id=course_id, value=value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
        
    
course = CRUDCourse(Course)
course_rating = CRUDCourseRating(CourseRating)
