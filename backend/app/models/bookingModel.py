from sqlalchemy import Column, Integer, String,  ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base



class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    seats_booked = Column(Integer, nullable=False)
    payment_status = Column(String, default="pending", nullable=False)

    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")