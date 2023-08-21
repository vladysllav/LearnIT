from fastapi import APIRouter
from app.api.users import routes as user_routes
from app.api.auth import routes as auth_routes

api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
