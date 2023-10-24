from typing import Union, Dict, Any
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.course import CourseCreate, CourseUpdate
from app.models.course import Course
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
    
    
    def update(self, db: Session, db_obj: Course, current_user: User,
               obj_in: Union[CourseUpdate, Dict[str, Any]]) -> Course:
        if not (current_user.id == db_obj.created_by_id or user.is_superuser(current_user)):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this course",
            )
            
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
        
    
course = CRUDCourse(Course)