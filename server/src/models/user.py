from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, EmailStr, Field
from beanie import Document


class Register(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str


class Login(BaseModel):
    email: EmailStr
    password: str


class User(Document):
    email: EmailStr
    username: str
    password: str
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "users"
