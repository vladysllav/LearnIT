from fastapi import APIRouter
from .views import UserView

router = APIRouter()

router.add_route("/", UserView, methods=["GET", "POST"])
