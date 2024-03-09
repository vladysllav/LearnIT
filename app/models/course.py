from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.base import TimestampedModel
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property


user_course_association = Table('user_course_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('course_id', Integer, ForeignKey('course.id'))
)


class Course(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, nullable=True)
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_by = relationship("User", back_populates='created_courses')
    users = relationship("User", secondary=user_course_association, back_populates="courses")
    modules = relationship("Module", back_populates="course")
    course_ratings = relationship("CourseRating", back_populates="course")

    @hybrid_property
    def average_rating(self):
        if not self.course_ratings:
            return None
        return sum(rating.rating_value for rating in self.course_ratings) / len(self.course_ratings)


class CourseRating(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    rating_value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    course = relationship("Course", back_populates="course_ratings")

    __table_args__ = (UniqueConstraint('user_id', 'course_id', name='unique_user_course_rating'),)
