from sqlalchemy.orm import Session
from ..models.eventModel import Event
from .errorHandleUtil import not_found_error
from typing import Any, Dict

# Find event_id in database
def get_event_or_404(db: Session, event_id: int) -> Event:
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        not_found_error("Event")
    
    return db_event

# 
def apply_event_update(db: Session, event: Event, updates: Dict[str, Any]) -> Event:
    """
    Sets each key/value on the event, commits & refreshes,
    then returns the updated instance
    """
    for attr, val in updates.items():
        setattr(event, attr, val)
    db.commit()
    db.refresh(event)
    return event