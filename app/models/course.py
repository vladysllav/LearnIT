from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base


user_course_association = Table('user_course_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_by = relationship("User", back_populates='created_courses')
    users = relationship("User", secondary=user_course_association, back_populates="users")
