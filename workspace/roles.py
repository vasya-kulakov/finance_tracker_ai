from pydantic import BaseModel
from typing import Optional, Tuple

class Parent(BaseModel):
    '''ID i add until the moment integration with PostGres'''
    id: int 
    role: str = 'Parent'
    name: str
    last_name: Optional[str]
    


class Children(BaseModel):
    '''ID i add until the moment integration with PostGres'''
    id: int
    role: str = 'Child'
    name: str
    last_name: Optional[str]


