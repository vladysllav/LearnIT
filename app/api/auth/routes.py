from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app import crud, models, schemas
from app.dependencies.base import get_db
from app.dependencies.users import get_current_user, get_current_active_user
from app.core.security import get_password_hash, decode_refresh_token, create_access_token, create_refresh_token
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


@router.post("/login", response_model=schemas.TokenResponse)
def login_access_token(
        db: Session = Depends(get_db),
        user_data: schemas.UserLogin = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=user_data.email, password=user_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(user_id=user.id, user_email=user.email)
    refresh_token = create_refresh_token(user_id=user.id, user_email=user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/token-refresh", response_model=schemas.RefreshTokenResponse)
def token_refresh(
        token: schemas.RefreshToken,
        db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Refresh access token by the refresh token
    """
    payload = decode_refresh_token(token.refresh_token)

    user_id = payload.get("sub", None)
    user_email = payload.get("email", None)
    if not user_id or not user_email:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token.")

    user = db.query(User).filter(and_(User.id == int(user_id), User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=401, detail=f"The user belonging to this token no logger exist")

    access_token = create_access_token(user_id=user.id,
                                       user_email=user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/me", response_model=schemas.User)
def me(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Endpoint that return user info from jwt token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}


@router.post("/sign-up", response_model=schemas.SignUpResponse)
def sign_up(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserSignUp,
) -> Any:
    """
    Sign Up as a new student.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)

    access_token = create_access_token(user_id=user.id, user_email=user.email)
    refresh_token = create_refresh_token(user_id=user.id, user_email=user.email)

    user_detail = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "type": user.type,
        "created_at": user.created_at
    }
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    return {
        "user_detail": user_detail,
        "tokens": tokens
    }
