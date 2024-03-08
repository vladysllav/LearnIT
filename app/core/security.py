from datetime import datetime, timedelta, timezone
from typing import Any, Union, Dict

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
        user_id: Union[str, Any], user_email: Union[str, Any]
) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(user_id), "email": str(user_email)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(
        user_id: Union[str, Any], user_email: Union[str, Any]
) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(user_id), "email": str(user_email)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, str]:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        exp_datetime = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)

        return decoded_token if exp_datetime >= datetime.now(timezone.utc) else None
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def decode_refresh_token(token: str) -> dict[str, str]:
    try:
        decoded_token = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        exp_datetime = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)

        return decoded_token if exp_datetime >= datetime.now(timezone.utc) else None
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def create_activation_url(user_id: int, user_email: str) -> str:
    expire_delta = timedelta(days=7)
    expire = datetime.utcnow() + expire_delta
    to_encode = {'exp': expire, 'sub': str(user_id), 'email': str(user_email)}
    token = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    url = f'{settings.DOMAIN_NAME}/{settings.API_STR}/users/activate/{token}'
    return url


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
