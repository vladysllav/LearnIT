from typing import List

from fastapi import APIRouter, Depends, Depends
from sqlalchemy.orm import Session

from app.dependencies.lessons import get_lessons
from app.models import Lessons
from app.models.user import User, UserType
from app.models.course import Course
from app.models.module import Module

from app.crud.crud_course import course as crud_course
from app.crud.crud_module import module as crud_module
from app.schemas.course import CourseUpdate, CourseCreate
from app.schemas.lessons import LessonsCreate, LessonsUpdate
from app.schemas.module import ModuleCreate, ModuleUpdate

from app.dependencies.base import get_db
from app.dependencies.users import get_current_user, PermissionChecker
from app.dependencies.course import get_course, check_course_access, get_module

from app.crud.crud_lessons import lessons as crud_lessons

router = APIRouter()
allow_create_resource = PermissionChecker([UserType.admin, UserType.superadmin])


@router.get('/')
def read_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    courses = crud_course.get_list(db, skip=skip, limit=limit)
    return courses


@router.get('/{course_id}')
def read_course_by_id(course: Course = Depends(get_course)):
    return course


@router.post('/',dependencies=[Depends(allow_create_resource)])
def create_course(*, db: Session = Depends(get_db), course_in: CourseCreate,
                  current_user: User = Depends(get_current_user)):
    course = crud_course.create(db, obj_in=course_in, current_user=current_user)

    return course


@router.put('/{course_id}', dependencies=[Depends(allow_create_resource)])
def update_course(*, db: Session = Depends(get_db),
                  course: Course = Depends(get_course),
                  course_in: CourseUpdate):
    course = crud_course.update(db, db_obj=course, obj_in=course_in)
    return course


@router.get('/{course_id}/modules/{module_id}' , )
def read_module_by_id(course: Course = Depends(get_course),
                      module: Module = Depends(get_module)):
    return module


@router.get('/{course_id}/modules/')
def read_all(db: Session = Depends(get_db),
             course: Course = Depends(get_course),
             skip: int = 0, limit: int = 100):
    modules = crud_module.get_list(db, skip=skip, limit=limit)
    return modules


@router.post('/{course_id}/modules/', dependencies=[Depends(allow_create_resource)])
def create_module(*, db: Session = Depends(get_db),
                  course_if_access: None = Depends(check_course_access),
                  module_in: ModuleCreate,
                  current_user: User = Depends(get_current_user),
                  course_id: int):
    module = crud_module.create(db, obj_in=module_in, course_id=course_id,
                                current_user=current_user)
    return module


@router.patch('/{course_id}/modules/{module_id}',dependencies=[Depends(allow_create_resource)])
def update_module(*, db: Session = Depends(get_db), module_in: ModuleUpdate,
                  course_access: None = Depends(check_course_access),
                  module: Module = Depends(get_module)):
    module = crud_module.update(db, db_obj=module, obj_in=module_in)
    return module



@router.delete('/{course_id}/modules/{module_id}',dependencies=[Depends(allow_create_resource)])
def remove_module(*, db: Session = Depends(get_db),
                  course_access: None = Depends(check_course_access),
                  module_id: int):
    module = crud_module.remove(db, id=module_id)
    return module


@router.post("/{course_id}/modules/{module_id}/lessons/{lessons_id}",dependencies=[Depends(allow_create_resource)])
def create_lessons(*, db: Session = Depends(get_db), lesson_in: LessonsCreate,
                   current_user: User = Depends(get_current_user),
                   module: Module = Depends(get_module),
                   course_access: None = Depends(check_course_access)):
    lesson = crud_lessons.create(db, obj_in=lesson_in, current_user=current_user, module_id=module.id)
    return lesson

@router.get('/{course_id}/modules/{module_id}/lessons/{lessons_id}')
def get_lessons(lessons: Lessons = Depends(get_lessons),
                module: Module = Depends(get_module)
                ,course_access: None = Depends(check_course_access)):
    return lessons


@router.get('/{course_id}/modules/{module_id}/lessons/')
def get_lessons_all(db: Session = Depends(get_db),
             module: Module = Depends(get_module)
            ,course_access: None = Depends(check_course_access),
             skip: int = 0, limit: int = 100):
    lessons = crud_lessons.get_list(db, skip=skip, limit=limit)
    return lessons


@router.put('/{course_id}/modules/{module_id}/lessons/{lesson_id}',dependencies=[Depends(allow_create_resource)])
def update_lesson(*, db: Session = Depends(get_db),
                  module: Module = Depends(get_module),
                  lesson: Lessons = Depends(get_lessons),
                  lesson_in: LessonsUpdate,
                  course_access: None = Depends(check_course_access)):
    lesson = crud_lessons.update(db, db_obj=lesson, obj_in=lesson_in)
    return lesson


@router.patch('/{course_id}/modules/{module_id}/lessons/{lesson_id}',dependencies=[Depends(allow_create_resource)])
def update_lesson(*, db: Session = Depends(get_db),
                  module: Module = Depends(get_module),
                  lesson: Lessons = Depends(get_lessons),
                  lesson_in: LessonsUpdate
                  ,course_access: None = Depends(check_course_access)):
    lesson = crud_lessons.update(db, db_obj=lesson, obj_in=lesson_in)
    return lesson


@router.delete('/{course_id}/modules/{module_id}/lessons/{lesson_id}',dependencies=[Depends(allow_create_resource)])
def delete_lesson(*, db: Session = Depends(get_db),
                  module: Module = Depends(get_module),
                  lesson_id: int,
                  course_access: None = Depends(check_course_access)):
    lessons = crud_lessons.remove(db, id=lesson_id)
    return lessons