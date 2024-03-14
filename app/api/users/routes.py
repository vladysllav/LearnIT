from datetime import date
from app.models import Course
from app.schemas.course import CourseRead
from app.schemas.user import CreateUserToInvite, UserSignUp, User
from app.services.user_service import InvitationService, UserService

from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies.base import get_db, get_pagination_params
from app.dependencies.users import get_current_active_user, get_current_active_superuser, get_invitation_service, \
    get_user_service, get_current_user
from app.core.config import settings

router = APIRouter()


@router.get("/alive")
def alive():
    return {'status': 'ok'}


@router.get("/", response_model=List[schemas.User])
def read_users(
        response: Response,
        db: Session = Depends(get_db),
        pagination: dict = Depends(get_pagination_params),
        current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve paginated users response
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    users = crud.user.get_list(db, skip=skip, limit=limit)
    total = crud.user.get_total_count(db)

    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Offset"] = str(skip)
    response.headers["X-Limit"] = str(limit)

    return users


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.post('/invite/')
def ivnite_user(user_schema: CreateUserToInvite,
                is_admin: models.User = Depends(get_current_active_superuser),
                invitation_service: InvitationService = Depends(get_invitation_service),
                user_service: UserService = Depends(get_user_service)) -> Any:
    new_user = user_service.create_user(user_schema)
    return invitation_service.invite_user(new_user)


@router.post('/activate/{token}')
def activate_user(user_schema: UserSignUp, token: str,
                  invitation_service: InvitationService = Depends(get_invitation_service)) -> Any:
    return invitation_service.activate_user(user_schema, token)


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
        *,
        db: Session = Depends(get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        first_name: str = Body(None),
        last_name: str = Body(None),
        date_of_birth: date = Body(None),
        phone_number: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password,
                                 email=email,
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number,
                                 date_of_birth=date_of_birth)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        current_user: models.User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.get("/users/{user_id}/courses", response_model=List[CourseRead])
def get_user_courses(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) \
        -> List[CourseRead]:
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user_courses = db.query(Course).filter_by(created_by_id=user_id).all()

    return [CourseRead.from_orm(course) for course in user_courses] if user_courses else []

