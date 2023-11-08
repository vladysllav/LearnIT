from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.models.user import User, UserType, Invitation
from app.repositories.base_repository import BaseRepository
from app.models.user import User



class UserRepository(BaseRepository):
    model = User
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db)


    def get_by_email(self, email: str) -> User:
        return self.db.query(self.model).filter(self.model.email == email).first()
    

    def authenticate(self, email: str, password: str) -> User:
        user = self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    

    def is_active(self, user: User) -> bool:
        return user.is_active
    

    def is_superuser(self, user: User) -> bool:
        return user.type == UserType.superadmin
    


class InvitationRepository(BaseRepository):
    model = Invitation
    def __init__(self, db):
        self.db = db
        super().__init__(db)

    
    def get_by_email(self, email: str) -> User:
        return self.db.query(self.model).filter(self.model.email == email).first()

    
    