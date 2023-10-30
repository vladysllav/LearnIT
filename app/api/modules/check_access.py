from fastapi import HTTPException
from app.models.course import Course
from app.models.module import Module
from app.models.user import User
from sqlalchemy.orm import Session
from app.crud.crud_user import user

def check_course_existence(db: Session, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

def check_module_existence(db: Session, module_id: int):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

def readability_check(db: Session, course_id: int, module_id: int = None):
    check_course_existence(db, course_id)
    
    if module_id is not None:
        check_module_existence(db, module_id)
    elif not db.query(Module).filter(Module.course_id == course_id).first():
        raise HTTPException(status_code=404, detail="No modules found in the specified course")
    
    
def acessibility_check(db: Session, course_id: int, current_user: User):
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course or not \
            (course.created_by_id == current_user.id and user.is_superuser(current_user)):
        raise HTTPException(status_code=404, detail="Course not found")

        

