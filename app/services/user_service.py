from app.repositories.base_repository import BaseRepository
from app.schemas.user import CreateUserForInvitation
from app.utils import generate_random_password
from app.core.security import get_password_hash


class UserService:
    def __init__(self, user_repo: BaseRepository):
        self.user_repo = user_repo


    def create_user(self, user: CreateUserForInvitation):
        user_data = user.dict()
        user_data['hashed_password'] = get_password_hash(generate_random_password())
        schema = CreateUserForInvitation(**user_data)
        return self.user_repo.create(schema)
    

