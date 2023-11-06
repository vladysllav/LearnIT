import os
import secrets
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api"
    SECRET_KEY: str = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = 'learnit'
    SERVER_HOST: str = '0.0.0.0'
    SERVER_PORT: int = 8000
    RELOAD: bool = True
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'learnit'
    SENTRY_DSN: Optional[HttpUrl] = ''

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    # POSTGRES_SERVER: str = 'localhost:5432'
    POSTGRES_SERVER: str = f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}'
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    USERS_OPEN_REGISTRATION: bool = False
    EMAILS_ENABLED: bool = True

    EMAILS_FROM_NAME: str = os.getenv("EMAILS_FROM_NAME")
    EMAILS_FROM_EMAIL: EmailStr = os.getenv("EMAILS_FROM_EMAIL")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: str = os.getenv("SMTP_PORT")
    SMTP_TLS: bool = os.getenv("SMTP_TLS")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

    class Config:
        case_sensitive = True


settings = Settings()
