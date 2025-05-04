from datetime import datetime, timedelta
from ..models.tempReserveModel import TempReservation
from ..models.eventModel import Event
from ..models.userModel import User
from sqlalchemy.orm import Session
from ..utils.eventUtil import get_event_or_404
from ..utils.errorHandleUtil import insufficient_seat
from ..enum.tempReserveEnum import RESERVATION_DURATION_MINUTES

def create_temp_reservation(db: Session, user: User, event_id: int, seats_requested: int) -> TempReservation:
    event = get_event_or_404(db, event_id)

    if event.available_seats < seats_requested:
        insufficient_seat()

    # Calculate expiration time
    expiration_time = datetime.utcnow() + timedelta(minutes=RESERVATION_DURATION_MINUTES)

    # Create reservation object
    temp_reservation = TempReservation(
        user_id=user.id,
        event_id=event.id,
        seats_reserved=seats_requested,
        reservation_time=datetime.utcnow(),
        expiration_time=expiration_time,
        status="pending"
    )

    # Reduce available seats temporarily
    event.available_seats -= seats_requested

    db.add(temp_reservation)
    db.commit()
    db.refresh(temp_reservation)

    return temp_reservation


