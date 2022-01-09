from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContentBase(BaseModel):
    id: int
    title: str
    story: str
    user_id: int
    total_likes: int
    total_reads: int
    date_published: datetime

    class Config:
        orm_mode = True


class ContentCreate(BaseModel):
    title: str
    story: str
    user_id: int
    date_published: datetime


class ContentUpdate(BaseModel):
    id: int
    title: Optional[str]
    story: Optional[str]
    likeordislike: Optional[str]
    readorunread: Optional[str]
