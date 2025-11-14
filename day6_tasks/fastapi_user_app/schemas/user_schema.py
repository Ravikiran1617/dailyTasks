from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"   # default role = user


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: str
