from sqlalchemy.orm import Session
from ..models.eventModel import Event
from .errorHandleUtil import not_found_error


# Find event_id in database
def get_event_or_404(db: Session, event_id: int) -> Event:
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        not_found_error("Event")
    
    return db_event


