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

    def update_course_rating(self, db: Session, course_id: int):
        course = db.query(self.model).filter(self.model.id == course_id).first()

        course.rating = course.average_rating
        db.commit()

        return course


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
            rating_value: int
    ) -> CourseRating:
        # Перевірка на допустимий діапазон рейтингу
        if not (0 <= rating_value <= 5):
            raise HTTPException(status_code=400, detail="Invalid rating. Must be between 0 and 5.")

        # Перевірка існування рейтингу для користувача та курсу
        existing_rating = self.get(db=db, user_id=user_id, course_id=course_id)
        if existing_rating:
            raise HTTPException(status_code=400, detail="You have already rated this course.")

        # Створення нового рейтингу
        db_obj = self.model(user_id=user_id, course_id=course_id, rating_value=rating_value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_ratings_for_course(self, db: Session, *, course_id: int):
        return db.query(self.model).filter(self.model.course_id == course_id).all()
        
    
course = CRUDCourse(Course)
course_rating = CRUDCourseRating(CourseRating)
