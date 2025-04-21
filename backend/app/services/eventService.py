from fastapi import status
from pydantic import BaseModel
from ..models.eventModel import Event
from ..schemas.eventSchema import (
    EventCreate,
    EventUpdate,
    EventResponse
)
from sqlalchemy.orm import Session
from ..utils.errorHandleUtil import (
    seats_negative_error,
    available_seats_exceed_error,
    not_found_error,    
    validate_event_status,
    invalid_eventStatus_transition_error,
    validate_eventStatus_transition,
    restricted_field_edit_error
)
from ..utils.eventUtil import get_event_or_404


# Check the values of total_seats and available_seat
def validate_seats_logic(total_seats: int, available_seats: int):
    if total_seats < 0 or available_seats < 0:
        seats_negative_error()
    if available_seats > total_seats:
        available_seats_exceed_error()

# Fetch all events
def get_all_events(db: Session):
    return db.query(Event).all()

# Get an event by id
def fetch_event_by_id(db: Session, event_id: int):
    return get_event_or_404(db, event_id)

# Create new event
def create_event(db: Session, event: EventCreate):
    validate_seats_logic(event.total_seats, event.available_seats)

    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {"message": "Event successfully created"}, status.HTTP_201_CREATED

# Search events by name
def search_event_by_name(db: Session, query: str):
    return db.query(Event).filter(Event.event_name.ilike(f"%{query}%")).all()

# Search events by time range
def search_event_by_datetime(db: Session, start_search, end_search):
    return db.query(Event).filter(
        Event.start_time >= start_search,
        Event.end_time <= end_search
    ).all()

# Update event name

def update_event(db: Session, event_id: int, event_update: EventUpdate) -> EventResponse:
    db_event = get_event_or_404(db, event_id)

    if not db_event:
        return None
    
    update_data = event_update.dict(exclude_unset=True)
    
    # Validate status transition
    if "status" in update_data:
        validate_eventStatus_transition(db_event.status, event_update.status.value)

    # Validate seat logic
    new_total = update_data.get("total_seats", db_event.total_seats)
    new_available = update_data.get("available_seats", db_event.available_seats)

    if new_available > new_total:
        available_seats_exceed_error()
    
    # Apply updates
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)

    return EventResponse.from_orm(db_event)



# Cancel an event by id
def cancel_event(db: Session, event_id: int):
    db_event = get_event_or_404(db, event_id)
    
    if db_event.status in {"completed", "cancelled"}:
        invalid_eventStatus_transition_error(db_event.status, "cancelled")
    
    db_event.status = "cancelled"
    db.commit()
    db.refresh(db_event)

    return {"message": "Event cancelled successfully", "event": db_event}
