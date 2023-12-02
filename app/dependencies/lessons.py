from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.dependencies.base import get_db
from app.models import Lessons


def get_lessons(lessons_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lessons).filter(Lessons.id == lessons_id).first()
    if not lessons:
        raise HTTPException(status_code=404, detail="Course not found")

    return lessons
