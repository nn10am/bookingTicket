from sqlalchemy.orm import Session
from datetime import datetime
from ..models.tempReserveModel import TempReservation
from ..models.eventModel import Event

# Free up expired reservations
def clean_expired_temp_reservations(db: Session):
    now = datetime.utcnow()
    expired = db.query(TempReservation).filter(TempReservation.expiration_time < now).all()

    for r in expired:
        event = db.query(Event).filter(Event.id == r.event_id).first()
        if event:
            event.available_seats += r.seats_reserved
        db.delete(r)
    
    db.commit()