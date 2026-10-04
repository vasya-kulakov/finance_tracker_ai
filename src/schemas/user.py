from typing import Optional
from pydantic import BaseModel


# Схемы для Parent (родитель)
class ParentBase(BaseModel):
    name: str
    last_name: Optional[str] = None


class ParentCreate(ParentBase):
    password: str


class Parent(ParentBase):
    id: int

    model_config = {"from_attributes": True}


class ParentInDB(ParentBase):
    hashed_password: str


# Схемы для Children (ребёнок)
class ChildrenBase(BaseModel):
    name: str
    last_name: Optional[str] = None
    parent_id: int


class ChildrenCreate(ChildrenBase):
    password: Optional[str] = None


class Children(ChildrenBase):
    id: int
    model_config = {"from_attributes": True}


class ChildrenInDB(ChildrenBase):
    hashed_password: Optional[str] = None
