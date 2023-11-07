from sqlalchemy import Column, Integer, String, Boolean, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.base import TimestampedModel
from app.models.course import user_course_association
from enum import Enum as PyEnum


class UserType(PyEnum):
    student = "student"
    admin = "admin"
    superadmin = "superadmin"


class InvitationStatus(PyEnum):
    active = 'active'
    accepted = 'accepted'
    canceled = 'canceled'


class User(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    type = Column(Enum(UserType), default=UserType.student)
    is_active = Column(Boolean, default=True)
    date_of_birth = Column(Date, nullable=True)
    phone_number = Column(String, nullable=True)
    created_courses = relationship("Course", back_populates="created_by")
    courses = relationship("Course", secondary=user_course_association, back_populates="users")
    invitation = relationship("Invitation", back_populates="user", uselist=False)


class Invitation(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    email = Column(String, unique=True, index=True)
    status = Column(Enum(InvitationStatus), default = InvitationStatus.active)


