from typing import Optional
from pydantic import Field
from pydantic import BaseModel


class BaseModule(BaseModel):
    title: Optional[str] = Field(None, example='Lessons FastApi')
    content: Optional[str] = Field(None, example='FastAPI is a modern, fast (high-performance)')
    module_id:Optional[int] = Field(None, example='1')

class LessonsCreate(BaseModule):
    pass


class LessonsUpdate(BaseModule):
    pass
