from pydantic import BaseModel
from datetime import datetime
from ..enum.paymentStatusEnum import PaymentStatus

class BookingCreate(BaseModel):
    event_id: int
    seats_booked: int
    payment_status: PaymentStatus

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int
    payment_status: str
    booking_time: datetime

    class Config:
        orm_mode = True