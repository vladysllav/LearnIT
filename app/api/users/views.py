from fastapi import HTTPException
from .models import User
from app.core.database import SessionLocal

class UserView:
    def __init__(self):
        self.db = SessionLocal()

    async def get(self):
        users = self.db.query(User).all()
        return {"users": users}

    async def post(self, user: User):
        self.db.add(user)
        self.db.commit()
        return {"user": user}

    def __del__(self):
        self.db.close()
