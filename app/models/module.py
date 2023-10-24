from sqlalchemy import Column, Integer, String, LargeBinary
from app.models.base import TimestampedModel
from app.db.base_class import Base



class Module(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=True)
    