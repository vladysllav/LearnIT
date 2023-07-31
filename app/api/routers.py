from fastapi import APIRouter
from app.api.users import views as user_routes

api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
