from fastapi import Query
from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    return {"skip": skip, "limit": limit}
    