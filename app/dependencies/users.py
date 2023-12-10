from app.models import User
from app.models.user import UserType
from app.repositories.user_repository import InvitationRepository, UserRepository
from app.services.user_service import InvitationService, UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud, models, schemas
from app.core.security import decode_token
from app.api.auth_bearer import JWTBearer
from app.dependencies.base import get_db

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_STR}/login/access-token"
# )


jwt_bearer = JWTBearer()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(jwt_bearer)
) -> models.User:
    try:
        payload = decode_token(token)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def invitation_service(db: Session = Depends(get_db)):
    return InvitationService(UserRepository(db), InvitationRepository(db))


def user_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))


def check_permission(current_user: models.User = Depends(get_current_user)):
    if current_user.type != UserType.admin and current_user.type != UserType.superadmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access forbidden, admin rights required")
