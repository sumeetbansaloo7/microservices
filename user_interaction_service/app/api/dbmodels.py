from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class EventLike(Base):
    __tablename__ = "eventlike"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    contentid = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=False)
    likedflag = Column(Boolean, nullable=False, server_default='False')
    latest_event_date = Column(TIMESTAMP(timezone=True),
                               nullable=False, server_default=text('now()'))


class EventRead(Base):
    __tablename__ = "eventread"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    contentid = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=False)
    readflag = Column(Boolean, nullable=False, server_default='False')
    latest_event_date = Column(TIMESTAMP(timezone=True),
                               nullable=False, server_default=text('now()'))
