from fastapi import APIRouter
from app.api.users import routes as user_routes
from app.api.auth import routes as auth_routes
from app.api.courses import routes as course_routes
from app.api.lessons import routes as lessons_routes


api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(course_routes.router, prefix="/courses", tags=["courses"])
api_router.include_router(lessons_routes.router, prefix="/lessons", tags=["lessons"])
