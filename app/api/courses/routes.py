from fastapi import APIRouter, Depends, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.crud.crud_course import course as crud_course
from app.schemas.course import CourseUpdate, CourseCreate
from app.dependencies.base import get_db
from app.dependencies.users import get_current_user


router = APIRouter()


@router.post('/')
def read_courses(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    courses = crud_course.get_multi(db, skip=skip, limit=limit)
    return courses


@router.post('/create')
def create_course(*, db: Session = Depends(get_db), course_in: CourseCreate,
                  current_user: User = Depends(get_current_user)):
    course = crud_course.create(db, obj_in=course_in, current_user=current_user)
    
    return course


@router.post('/update/{course_id}')
def update_course(*, db: Session = Depends(get_db), course_id: int,
                  course_in: CourseUpdate, current_user: User = Depends(get_current_user)):
    course = crud_course.get(db, id=course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
   
    course = crud_course.update(db, db_obj=course, obj_in=course_in, current_user=current_user)
    return course