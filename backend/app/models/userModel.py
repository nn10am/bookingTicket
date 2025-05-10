from ..db.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False) 
    hashed_password = Column(String, nullable=False)    
    is_admin = Column(Boolean, default=False)

    # Relationships
    bookings = relationship('Booking', back_populates='user')

    class Config:
        from_attributes = True