from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.models.user import User



class UserRepository(BaseRepository):
    model = User
    def __init__(self, db):
        self.db = db
        super().__init__(db, self.model)

    