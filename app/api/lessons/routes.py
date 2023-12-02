from app.dependencies.base import get_db
from app.dependencies.lessons import get_lessons
from app.dependencies.users import get_current_user
from app.crud.crud_lessons import lessons as crud_lessons

from app.models import User, Lessons

from app.schemas.lessons import LessonsCreate, LessonsUpdate

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")

def lessons_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    lessons = crud_lessons.get_list(db, skip=skip, limit=limit)
    return lessons

@router.get('/{lessons_id}')
def get_lessons(lessons: Lessons = Depends(get_lessons)):
    return lessons


@router.post("/")
def create_lessons(*, db: Session = Depends(get_db), course_in: LessonsCreate,
                   current_user: User = Depends(get_current_user)):
    course = crud_lessons.create(db, obj_in=course_in, current_user=current_user)

    return course


@router.put('/{lessons_id}')
def update_course(*, db: Session = Depends(get_db),
                  lessons: Lessons = Depends(get_lessons),
                  lessons_in: LessonsUpdate):
    lessons = crud_lessons.update(db, db_obj=lessons, obj_in=lessons_in)
    return lessons


@router.delete('/{lessons_id}')
def delete_lessons(*, db: Session = Depends(get_db),
                  lessons_id: int):
    lessons=crud_lessons.remove(db,id=lessons_id)
    return lessons