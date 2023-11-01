from fastapi import APIRouter, Depends, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.course import Course
from app.models.module import Module

from app.crud.crud_course import course as crud_course
from app.crud.crud_module import module as crud_module
from app.schemas.course import CourseUpdate, CourseCreate
from app.schemas.module import ModuleCreate, ModuleUpdate

from app.dependencies.base import get_db
from app.dependencies.users import get_current_user
from app.dependencies.course import get_course, check_course_access, get_module



router = APIRouter()


@router.get('/')
def read_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    courses = crud_course.get_list(db, skip=skip, limit=limit)
    return courses


@router.get('/{course_id}')
def read_course_by_id(course: Course = Depends(get_course)):
    return course


@router.post('/')
def create_course(*, db: Session = Depends(get_db), course_in: CourseCreate,
                  current_user: User = Depends(get_current_user)):
    course = crud_course.create(db, obj_in=course_in, current_user=current_user)
    
    return course


@router.put('/{course_id}')
def update_course(*, db: Session = Depends(get_db),
                  course: Course = Depends(get_course),
                  course_in: CourseUpdate):
   
    course = crud_course.update(db, db_obj=course, obj_in=course_in)
    return course

@router.get('/{course_id}/modules/{module_id}')
def read_module_by_id(course: Course = Depends(get_course),
                      module: Module = Depends(get_module)):
    
    return module
    
    
@router.get('/{course_id}/modules/')
def read_all(db: Session = Depends(get_db),
             course: Course = Depends(get_course),
             skip: int = 0, limit: int = 100):
    
    modules = crud_module.get_list(db, skip=skip, limit=limit)
    return modules
    
    
@router.post('/{course_id}/modules/')
def create_module(*, db: Session = Depends(get_db),
                  course_if_access: None = Depends(check_course_access),
                  module_in: ModuleCreate,
                  current_user: User = Depends(get_current_user),
                  course_id: int):

    module = crud_module.create(db, obj_in=module_in, course_id=course_id,
                                current_user=current_user)
    return module


@router.patch('/{course_id}/modules/{module_id}')
def update_module(*, db: Session = Depends(get_db), module_in: ModuleUpdate,
                  course_access: None = Depends(check_course_access),
                  module: Module = Depends(get_module)):
    
    module = crud_module.update(db, db_obj=module, obj_in=module_in)
    return module


@router.delete('/{course_id}/modules/{module_id}')
def remove_module(*, db: Session = Depends(get_db),
                  course_access: None = Depends(check_course_access),
                  module_id: int):
    
    module = crud_module.remove(db, id=module_id)
    return module