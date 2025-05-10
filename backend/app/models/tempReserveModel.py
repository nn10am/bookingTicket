from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
class TempReservation(Base):
    __tablename__ = "temp_reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    seats_reserved = Column(Integer, nullable=False)
    reservation_time = Column(DateTime, default=datetime.utcnow)
    expiration_time = Column(DateTime)
    status = Column(String, default="pending")

    # Relationships
    user = relationship('User', back_populates='temp_reservations')
    event = relationship('Event', back_populates='temp_reservations')