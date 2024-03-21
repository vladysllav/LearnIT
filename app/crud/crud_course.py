from typing import Union, Dict, Any
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.users import get_user
from app.dependencies.course import get_course
from app.schemas.course import CourseCreate, CourseUpdate, CourseRatingCreate, CourseUserAssociationUpdate
from app.models.course import Course, CourseRating, user_course_association
from app.crud.base import CRUDBase
from app.crud.crud_user import user
from app.models.user import User, UserType


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

    def add_user(self, db: Session, course: Course, user: User):

        if user.type is not UserType.student:
            raise HTTPException(status_code=400, detail="You can only add students to the course.")

        if user in course.users:
            raise HTTPException(status_code=400, detail="User already in the course.")

        course.users.append(user)
        db.commit()

        return course.users

    def remove_user(self, db: Session, course: Course, user: User):

        if user not in course.users:
            raise HTTPException(status_code=404, detail="User not in the course.")

        course.users.remove(user)
        db.commit()

        return course.users

    def update_users(
            self,
            db: Session,
            data: CourseUserAssociationUpdate,
            course_id: int,
            user_id: int
    ):

        course = get_course(data.course_id, db=db)
        user = get_user(data.user_id, db=db)

        if user.type is not UserType.student:
            raise HTTPException(status_code=400, detail="You can only add students to the course.")

        update_data = {}
        if data.user_id:
            update_data["user_id"] = data.user_id
        if data.course_id:
            update_data["course_id"] = data.course_id

        association = db.query(user_course_association).filter(
            user_course_association.c.user_id == user_id,
            user_course_association.c.course_id == course_id
        ).first()

        if not association:
            raise HTTPException(status_code=404, detail="Association not found. "
                                                        "Change your 'course_id' or 'user_id' in the parameters.")

        existing_association = db.query(user_course_association).filter(
            user_course_association.c.user_id == data.user_id,
            user_course_association.c.course_id == data.course_id
        ).first()

        if existing_association:
            raise HTTPException(status_code=400, detail="Association already exists. "
                                                        "Change your 'course_id' or 'user_id' in the dictionary.")

        db.query(user_course_association).filter(
            user_course_association.c.user_id == user_id,
            user_course_association.c.course_id == course_id
        ).update(update_data)

        res_association = db.query(user_course_association).filter(
            user_course_association.c.user_id == data.user_id,
            user_course_association.c.course_id == data.course_id
        ).first()

        db.commit()

        return {"course_id": res_association[1], "user_id": res_association[0]}


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
