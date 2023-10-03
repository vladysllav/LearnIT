from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
from enum import Enum as PyEnum



class UserType(PyEnum):
    student = "student"
    admin = "admin"
    superadmin = "superadmin"


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    type = Column(Enum(UserType), default=UserType.student)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_of_birth = Column(Date, nullable=True)
    phone_number = Column(String, nullable=True)
    items = relationship("Item", back_populates="owner")
    courses = relationship("Course", back_populates="lecturer")
    user_courses = relationship("UserCourse", back_populates="user")
