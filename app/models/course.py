from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .user import User


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lecturer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    lecturer = relationship(User, back_populates='courses')
    user_courses = relationship("UserCourse", back_populates="course")
