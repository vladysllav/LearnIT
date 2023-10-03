from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .user import User
from .course import Course


class UserCourse(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True, nullable=False)
    user = relationship(User, back_populates="user_courses")
    course = relationship(Course, back_populates="user_courses")
