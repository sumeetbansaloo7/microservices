from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    id: int
    contentid: int
    userid: int
    latest_event_date: datetime

    class Config:
        orm_mode = True


class EventBaseLiked(EventBase):
    likedflag: Optional[bool]

    class Config:
        orm_mode = True


class EventBaseRead(EventBase):
    readflag: bool

    class Config:
        orm_mode = True


class EvenLike(BaseModel):
    contentid: int
    email: EmailStr
    password: str


class EvenRead(BaseModel):
    contentid: int
    email: EmailStr
    password: str
