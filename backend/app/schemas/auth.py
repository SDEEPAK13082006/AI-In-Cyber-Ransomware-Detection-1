"""
Pydantic Schemas for Authentication & User Registration
"""

from pydantic import BaseModel
from typing import Optional

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "analyst"

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str

class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
