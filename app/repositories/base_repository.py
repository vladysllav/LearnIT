from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union


ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType')



class BaseRepository:
    model = None
    def __init__(self, db: Session):
        self.db = db


    def create(self, dict_data: dict) -> ModelType:
        model = self.model(**dict_data)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model


    def get_by_id(self, id: int) -> ModelType:
        return self.db.query(self.model).filter(self.model.id == id).first()
    

    def get_list(self, skip: int = 0, limit: int = 100) -> ModelType:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    

    def update(self, id: int, dict_data: SchemaType) -> ModelType:
        self.db.query(self.model).filter(self.model.id == id).update(dict_data)
        self.db.commit()
        return self.get_by_id(id)
    

    def delete(self, id: int) -> ModelType:
        query = self.db.query(self.model).filter(self.model.id == id).first()
        if not query:
            raise Exception
        self.db.delete(query)
        self.db.commit()
        return query