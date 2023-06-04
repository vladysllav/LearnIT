from fastapi import FastAPI
from app.api.routers import api_router
from app.core.database import Base, engine

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)
