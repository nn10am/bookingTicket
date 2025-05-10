from pydantic import BaseModel
from datetime import datetime

class TempReservationCreate(BaseModel):
    event_id: int
    seats_reserved: int

class TempReservationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_reserved: int
    reservation_time: datetime
    expiration_time: datetime
    status: str

    class Config:
        orm_mode = True
        