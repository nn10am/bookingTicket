from datetime import datetime, timedelta
from ..models.tempReserveModel import TempReservation
from ..models.eventModel import Event
from ..models.userModel import User
from ..models.bookingModel import Booking
from sqlalchemy.orm import Session
from ..utils.eventUtil import get_event_or_404
from ..utils.errorHandleUtil import insufficient_seat, not_found_error, invalid_or_expired_reservation, invalid_reservation_access
from ..enum.tempReserveEnum import RESERVATION_DURATION_MINUTES
from ..enum.paymentStatusEnum import PaymentStatus
from ..schemas.bookingSchema import BookingResponse

# Get a temporary reservation by ID
def get_temp_reservation_by_id(db: Session, reservation_id: int) -> TempReservation:
    reservation = db.query(TempReservation).filter(TempReservation.id==reservation_id).first()
    if not reservation:
        not_found_error("Reservation")
        
    # Check if the reservation access belongs to the right user
    if reservation.user_id != User.id:
        invalid_reservation_access()
    
    return reservation

def create_temp_reservation(db: Session, user: User, event_id: int, seats_requested: int) -> TempReservation:
    event = get_event_or_404(db, event_id)
    
    if not event:
        not_found_error("Event")

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

# Set temp reservations to be expired
def expire_temp_reservations(db: Session):
    now = datetime.utcnow()
    expired = db.query(TempReservation).filter(
        TempReservation.expiration_time < now,
        TempReservation.status == "pending"
    ).all()

    for res in expired:
        res.status == "expired"
        event = db.query(Event).filter(Event.id == res.event_id).first()
        if event:
            event.available_seats += res.seats_reserved
    
    db.commit()

# Move temp resereve to booking
def finalize_temp_reserevation(db: Session, reservation_id: int, user: User) -> Booking:
    reservation = db.query(TempReservation).filter(
        TempReservation.id == reservation_id,
        TempReservation.user_id == user.id,
        TempReservation.status == "pending",
        TempReservation.expiration_time > datetime.utcnow()
    ).first()

    if not reservation:
        invalid_or_expired_reservation()
    
    booking = Booking(
        user_id = user.id,
        event_id = reservation.event_id,
        seats_booked = reservation.seats_reserved,
        payment_status = PaymentStatus.paid.value,
        booking_time = datetime.utcnow()
    )

    reservation.status = "confirmed"

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return BookingResponse.from_orm(booking)



