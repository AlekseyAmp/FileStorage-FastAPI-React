from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from beanie import Document

class Register(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str

class Login(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr



class User(Document):

    class Settings:
        name = "users"

    email: EmailStr
    password: str
    created_at: Optional[datetime] = None
