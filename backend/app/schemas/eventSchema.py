from pydantic import BaseModel, Field
from datetime import datetime
from ..enum.eventStatusEnum import EventStatus
from typing import Optional


class EventBase(BaseModel):
    event_name: str
    venue: str
    total_seats: int
    available_seats: int
    status: EventStatus = EventStatus.scheduled
    start_time: datetime
    end_time: datetime

    class Config: 
        from_attributes = True
   
class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    event_name: Optional[str] = Field(None, min_length=1)
    venue: Optional[str] = Field(None, min_length=1)
    total_seats: Optional[int] = Field(None, ge=0)
    available_seats: Optional[int] = Field(None, ge=0)
    status: Optional[EventStatus] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    class Config:        
        from_attributes = True
        

class EventResponse(EventBase):
    event_id: int

    class Config:
        orm_mode = True
        from_attributes = True


        
class EventUpdateResponse(BaseModel):
    message: str
    event: EventResponse



    
