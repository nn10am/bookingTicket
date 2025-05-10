from sqlalchemy import Column, Integer, Float, String, DateTime, UniqueConstraint
from ..db.base import Base
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index = True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    venue = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    total_seats = Column(Integer, nullable=False, default=0)
    available_seats = Column(Integer, nullable=False, default=0)
    status = Column(String, default="scheduled")

    __table_args__ = (
        UniqueConstraint('event_name', 'venue', 'start_time', name='uix_event_name_venue_start'),
    )

    # Relationship
    bookings = relationship('Booking', back_populates='event')