from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime

from ..base import Base
from ..mixins import CRUDMixin

class ScheduleEntry(Base, CRUDMixin):
    __tablename__ = 'schedule_entries'

    id = Column('id', Integer, primary_key=True)
    start = Column('start', DateTime)
    end = Column('end', DateTime)
    title = Column('title', String())
    description = Column('description', String())
    visible = Column('visible', Boolean)
    game_id = Column('game_id', Integer, ForeignKey('games.id'), nullable=False)
    interview_id = Column('interview_id', Integer, ForeignKey('interviews.id'))
    prize_id = Column('prize_id', Integer, ForeignKey('prizes.id'))
