from datetime import datetime

from typing import Optional, Union
from pydantic import Field
from pydantic import BaseModel


class BaseModule(BaseModel):
    title: Optional[str] = Field(None, example='Python Operators')
    image: Optional[str] = Field(None, example='https://s3.amazonaws.com/basket/image.jpg')
    
    
class ModuleRead(BaseModule):
    id: Optional[int] = Field(None, example=1)
    created_at: Optional[datetime] = Field(None, example='2023-02-21')
    updated_at: Optional[datetime] = Field(None, example='2023-03-05')
    
    
class ModuleCreate(BaseModule):
    pass


class ModuleUpdate(BaseModule):
    pass