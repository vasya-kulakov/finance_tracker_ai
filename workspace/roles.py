from pydantic import BaseModel
from typing import Optional

class Parent(BaseModel):
    '''ID i add until the moment integration with PostGres'''
    id: int 
    name: str
    last_name: Optional[str]
    password: str
        

class Children(BaseModel):
    '''ID i add until the moment integration with PostGres'''
    id: int
    name: str
    last_name: Optional[str]
    password: str
    parent_id: int

