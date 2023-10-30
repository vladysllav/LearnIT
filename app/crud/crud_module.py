from typing import Union, Dict, Any
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.module import ModuleCreate, ModuleUpdate
from app.models.course import Course
from app.models.user import User
from app.models.module import Module
from app.crud.base import CRUDBase
from app.crud.crud_user import user



class CRUDModule(CRUDBase[Module, ModuleCreate, ModuleUpdate]):
    def create(self, db: Session, *, obj_in: ModuleCreate, course_id: int) -> Module:       
        module_data = obj_in.dict()
        module_data['course_id'] = course_id
        module_data['created_at'] = datetime.utcnow()
        
        db_obj = Module(**module_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
    def update(self, db: Session, *, db_obj: Module, course_id: int,
               obj_in: Union[ModuleUpdate, Dict[str, Any]]) -> Module:     
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
       
    
module = CRUDModule(Module)
            
        
        