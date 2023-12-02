from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base import TimestampedModel


class Lessons(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    module_id = Column(Integer, ForeignKey('module.id'))
    module = relationship("Module", back_populates="lessons")


