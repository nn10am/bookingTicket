from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from ..db.base import Base


class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index = True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    venue = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False, default=0)
    available_seats = Column(Integer, nullable=False, default=0)
    status = Column(String, default="scheduled")

    __table_args__ = (
        UniqueConstraint('event_name', 'venue', 'start_time', name='uix_event_name_venue_start'),
    )