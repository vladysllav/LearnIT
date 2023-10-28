from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import TimestampedModel
from app.db.base_class import Base



class Module(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("Course", back_populates="modules")
    