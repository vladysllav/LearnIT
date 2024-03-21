from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.lessons import get_lessons
from app.filters import CourseFilter
from app.models import Lessons
from app.models.user import User, UserType
from app.models.course import Course, user_course_association
from app.models.module import Module

from app.crud.crud_course import course as crud_course
from app.crud.crud_course import course_rating as crud_course_rating
from app.crud.crud_module import module as crud_module
from app.schemas.course import (CourseUpdate, CourseCreate, CourseRead, CourseRatingCreate, CourseRatingRead,
                                CourseUserAssociationUpdate)
from app.schemas.lessons import LessonsCreate, LessonsUpdate
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.schemas.user import User as UserSchema

from app.dependencies.base import get_db
from app.dependencies.users import get_user, get_current_user, PermissionChecker
from app.dependencies.course import get_course, check_course_access, get_module

from app.crud.crud_lessons import lessons as crud_lessons

from typing import List

router = APIRouter()
allow_create_resource = PermissionChecker([UserType.admin, UserType.superadmin])
allow_add_rating = PermissionChecker([UserType.student])


@router.get('/')
def read_all(filters: CourseFilter = Depends(), db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return filters.filter_courses(db, skip, limit)


@router.get('/{course_id}', response_model=CourseRead)
def read_course_by_id(course: Course = Depends(get_course)):
    return course


@router.post("/{course_id}/ratings", dependencies=[Depends(allow_add_rating)],
             response_model=CourseRatingRead)
def create_course_rating(
    course_id: int,
    rating_data: CourseRatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return crud_course_rating.create(
        db=db,
        user_id=current_user.id,
        course_id=course_id,
        **rating_data.dict()
    )


@router.post('/', dependencies=[Depends(allow_create_resource)])
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


@router.get("/{course_id}/users/", response_model=List[UserSchema])
def get_users_of_course(
        course: Course = Depends(get_course),
):
    return course.users


@router.post(
    "/{course_id}/users/{user_id}",
    response_model=List[UserSchema],
    dependencies=[Depends(allow_create_resource)])
def add_user_to_course(
        db: Session = Depends(get_db),
        course: Course = Depends(get_course),
        user: User = Depends(get_user),
):

    course_users = crud_course.add_user(db=db, course=course, user=user)
    return course_users


@router.patch("/courses/{course_id}/users/{user_id}", gitdependencies=[Depends(allow_create_resource)])
def update_users_in_course(
        course_id: int,
        user_id: int,
        data: CourseUserAssociationUpdate,
        db: Session = Depends(get_db),
):

    association = crud_course.update_users(db=db, data=data, course_id=course_id, user_id=user_id)
    return association


@router.delete(
    "/{course_id}/users/{user_id}",
    response_model=List[UserSchema],
    dependencies=[Depends(allow_create_resource)])
def remove_user_from_course(
        db: Session = Depends(get_db),
        course: Course = Depends(get_course),
        user: User = Depends(get_user),
):

    course_users = crud_course.remove_user(db=db, course=course, user=user)
    return course_users


@router.get('/{course_id}/modules/{module_id}', )
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
                  course_id: int):
    module = crud_module.create(db, obj_in=module_in, course_id=course_id)
    return module


@router.patch('/{course_id}/modules/{module_id}', dependencies=[Depends(allow_create_resource)])
def update_module(*, db: Session = Depends(get_db), module_in: ModuleUpdate,
                  course_access: None = Depends(check_course_access),
                  module: Module = Depends(get_module)):
    module = crud_module.update(db, db_obj=module, obj_in=module_in)
    return module


@router.delete('/{course_id}/modules/{module_id}', dependencies=[Depends(allow_create_resource)])
def remove_module(*, db: Session = Depends(get_db),
                  course_access: None = Depends(check_course_access),
                  module_id: int):
    module = crud_module.remove(db, id=module_id)
    return module


@router.post("/{course_id}/modules/{module_id}/lessons/{lessons_id}", dependencies=[Depends(allow_create_resource)])
def create_lessons(*, db: Session = Depends(get_db), lesson_in: LessonsCreate,
                   current_user: User = Depends(get_current_user),
                   module: Module = Depends(get_module),
                   course_access: None = Depends(check_course_access)):
    lesson = crud_lessons.create(db, obj_in=lesson_in, current_user=current_user, module_id=module.id)
    return lesson


@router.get('/{course_id}/modules/{module_id}/lessons/{lessons_id}')
def get_lessons(lessons: Lessons = Depends(get_lessons),
                module: Module = Depends(get_module),
                course_access: None = Depends(check_course_access)):
    return lessons


@router.get('/{course_id}/modules/{module_id}/lessons/')
def get_lessons_all(db: Session = Depends(get_db),
                    module: Module = Depends(get_module),
                    course_access: None = Depends(check_course_access),
                    skip: int = 0, limit: int = 100):
    lessons = crud_lessons.get_list(db, skip=skip, limit=limit)
    return lessons


@router.put('/{course_id}/modules/{module_id}/lessons/{lesson_id}', dependencies=[Depends(allow_create_resource)])
def update_lesson(*, db: Session = Depends(get_db),
                  module: Module = Depends(get_module),
                  lesson: Lessons = Depends(get_lessons),
                  lesson_in: LessonsUpdate,
                  course_access: None = Depends(check_course_access)):
    lesson = crud_lessons.update(db, db_obj=lesson, obj_in=lesson_in)
    return lesson


@router.delete('/{course_id}/modules/{module_id}/lessons/{lesson_id}', dependencies=[Depends(allow_create_resource)])
def delete_lesson(*, db: Session = Depends(get_db),
                  module: Module = Depends(get_module),
                  lesson_id: int,
                  course_access: None = Depends(check_course_access)):
    lessons = crud_lessons.remove(db, id=lesson_id)
    return lessons
