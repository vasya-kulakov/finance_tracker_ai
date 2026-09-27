from pydantic import BaseModel
from typing import Optional

class Parent(BaseModel):
    name: str
    last_name: Optional[str]
    password: str
        

class Children(BaseModel):
    name: str
    last_name: Optional[str]
    password: Optional[str]
    parent_id: int

