from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    story = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    total_likes = Column(Integer, nullable=False, server_default='0')
    total_reads = Column(Integer, nullable=False, server_default='0')
    date_published = Column(DateTime, nullable=False)
