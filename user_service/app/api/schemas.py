from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    id: int
    firstname: str
    lastname: str
    phone: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    new_email: Optional[EmailStr]
    new_password: Optional[str]


class UserDelete(BaseModel):
    email: EmailStr
    password: str


class UserValidte(UserDelete):
    pass
