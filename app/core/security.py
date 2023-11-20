from datetime import datetime, timedelta, timezone
from typing import Any, Union, Dict

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
        user_id: Union[str, Any], user_email: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(user_id), "email": str(user_email)}
    secret_key = settings.SECRET_KEY
    algorithm = ALGORITHM
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def create_activation_url(user_id: int, user_email: str) -> str:
    expire_delta = timedelta(days=7)
    expire = datetime.utcnow() + expire_delta
    to_encode = {'exp': expire, 'sub': str(user_id), 'email': str(user_email)}
    token = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    url = f'https://0.0.0.0:8000/api/users/activate/{token}'
    return url


def decode_token(token: str) -> dict:
    try:
        secret_key = settings.SECRET_KEY
        algorithm = ALGORITHM
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        exp_datetime = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)

        return decoded_token if exp_datetime >= datetime.now(timezone.utc) else None
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
