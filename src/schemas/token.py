from pydantic import BaseModel
from dataclasses import dataclass
from fastapi import Form

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None


@dataclass
class LoginForm:
    username: str = Form(...)
    password: str = Form(...)