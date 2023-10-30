from fastapi import APIRouter, Depends, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.crud.crud_module import module as crud_module 
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.dependencies.base import get_db
from app.dependencies.users import get_current_user
from app.api.modules.check_access import readability_check, acessibility_check


router = APIRouter()


@router.get('/{id}')
def read_module_by_id(module_id: int, course_id: int, db: Session = Depends(get_db)):
    readability_check(db, course_id=course_id, module_id=module_id)
    
    module = crud_module.get(db, id=module_id)
    return module
    
    
@router.get('/')
def read_all(course_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    readability_check(db, course_id=course_id)
    
    modules = crud_module.get_list(db, skip=skip, limit=limit)
    return modules
    
    
@router.post('/')
def create_module(*, db: Session = Depends(get_db), course_id: int, module_in: ModuleCreate,
                  current_user: User = Depends(get_current_user)):
    acessibility_check(db, course_id=course_id, current_user=current_user)
    
    module = crud_module.create(db, obj_in=module_in, course_id=course_id,
                                current_user=current_user)
    return module


@router.patch('/{id}')
def update_module(*, db: Session = Depends(get_db), id: int, module_in: ModuleUpdate,
                  course_id: int, current_user: User = Depends(get_current_user)):
    acessibility_check(db, course_id=course_id, current_user=current_user)
    
    module = crud_module.get(db=db, id=id)
    module = crud_module.update(db, db_obj=module, obj_in=module_in, course_id=course_id)
    return module


@router.delete('/{id}')
def remove_module(*, db: Session = Depends(get_db), id: int, course_id: int,
                  current_user: User = Depends(get_current_user)):
    acessibility_check(db, course_id=course_id, current_user=current_user)
    
    module = crud_module.remove(db, id=id, course_id=course_id)
    return module