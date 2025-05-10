from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..models.userModel import User
from ..schemas.userSchema import UserResponse
from ..schemas.tempReserveSchema import TempReservationCreate,TempReservationResponse
from ..schemas.bookingSchema import BookingResponse
from ..services.tempReserveService import create_temp_reservation, finalize_temp_reserevation, get_temp_reservation_by_id
from ..utils.errorHandleUtil import not_found_error, insufficient_seat, invalid_or_expired_reservation, invalid_reservation_access
from ..utils.dbUtil import get_db
from ..models.eventModel import Event
from ..utils.authUtil import get_current_user


router = APIRouter()

@router.get("/temp_reservations/{reservation_id}", response_model=TempReservationResponse)
async def get_temp_reservation_by_id_route(
    reservation_id: int,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user)
):
    reservation = get_temp_reservation_by_id(db, reservation_id)
    if not reservation:
        not_found_error("Temp reservation")

    if reservation.user_id != user.id:
        invalid_reservation_access()

    return reservation

# Create temp reserevation route
@router.post("/temp_reservations/", response_model=TempReservationResponse)
async def create_temp_reservation_route(
    temp_reservation: TempReservationCreate,
    db: Session = Depends(get_db),
    user: User = Depends

):
    event = db.query(Event).filter(Event.id == temp_reservation.event_id).first()

    if not event:
        not_found_error("Event")
    
    return create_temp_reservation(db=db, user=user, event_id=temp_reservation.event_id,
                                   seats_requested=temp_reservation.seats_reserved)