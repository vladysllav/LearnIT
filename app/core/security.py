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
    # print(f'Encode secret key = {secret_key}')
    # print(f'Encode algorithm = {algorithm}')
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    # print(f'Incoming token for decoding: {token}')
    try:
        secret_key = settings.SECRET_KEY
        algorithm = ALGORITHM
        # print(f'Decode secret key = {secret_key}')
        # print(f'Decode algorithm = {algorithm}')
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        # print(f'decoded_token: {decoded_token}')
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
