from app.repositories.user_repository import InvitationRepository, UserRepository
from app.services.user_service import InvitationService, UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app import crud, models, schemas
from app.core.security import decode_access_token
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
        payload = decode_access_token(token)
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



def user_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))


def invitation_service(db: Session = Depends(get_db)):
    return InvitationService(InvitationRepository(db))
        