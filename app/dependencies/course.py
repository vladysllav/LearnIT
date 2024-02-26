from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends, HTTPException, status
from app.dependencies.base import get_db
from app.models.course import Course
from app.models.module import Module
from app.models.user import User
from app.dependencies.users import get_current_user
from app.crud.crud_user import user


def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course


def get_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    
    return module


def check_course_access(
    course: Course = Depends(get_course), 
    current_user: User = Depends(get_current_user)):
    if course.created_by_id != current_user.id or not user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="You don't have permission for this course")
    
