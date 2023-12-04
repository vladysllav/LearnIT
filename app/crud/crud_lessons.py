from typing import Union, Dict, Any
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase, ModelType, UpdateSchemaType
from app.models import Lessons, User
from app.schemas.lessons import LessonsCreate, LessonsUpdate


class CRUDLesson(CRUDBase[Lessons, LessonsCreate, LessonsUpdate]):
    def create(self, db: Session, *,obj_in: LessonsCreate, current_user: User , module_id:int) -> Lessons:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")

        lesson_data = obj_in.dict()
        lesson_data['created_at'] = datetime.utcnow()
        lesson_data['module_id'] = module_id

        db_obj = Lessons(**lesson_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType,
    Dict[str, Any]]) -> Lessons:
        if isinstance(obj_in, dict):
            data_upd = obj_in
        else:
            data_upd = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=data_upd)


lessons = CRUDLesson(Lessons)
