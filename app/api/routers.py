from fastapi import APIRouter
from .users import routes as user_routes
from .courses import routes as course_routes

api_router = APIRouter()

api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(course_routes.router, prefix="/courses", tags=["courses"])
