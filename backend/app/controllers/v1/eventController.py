from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...schemas.eventSchema import EventCreate, EventUpdate, EventResponse
from ...services import eventService
from ...db.session import get_db
from ...config import API_VERSION

router = APIRouter(prefix=f"{API_VERSION['v1']}/events", tags=["Events"])


# Get all events
@router.get("/", response_model=List[EventResponse])
async def get_all_events(db: Session = Depends(get_db)):
    return eventService.get_all_events(db)

# Get an event by id
@router.get("/{event_id}")
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    return eventService.fetch_event_by_id(db, event_id)

# Search events by name
@router.get("/search/name", response_model=List[EventResponse])
async def search_event_by_name(query: str, db: Session = Depends(get_db)):
    return eventService.search_event_by_name(db, query)

# Search events by time range
@router.get("/search/date", response_model=List[EventResponse])
async def search_event_by_time_range(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    return eventService.search_event_by_datetime(db, start_date, end_date)

# Add an event
@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return eventService.create_event(db, event)[0]

# Update an event by id
@router.patch("/{event_id}", response_model=EventResponse)
async def update_event_by_id(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    return eventService.update_event(db, event_id, event_update)

# Cancel an event by id
@router.post("/{event_id}/cancel")
async def cancel_event_by_id(event_id: int, db: Session = Depends(get_db)):
    return eventService.cancel_event(db, event_id)

