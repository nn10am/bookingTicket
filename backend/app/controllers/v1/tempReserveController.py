from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...schemas.tempReserveSchema import TempReservationCreate, TempReservationResponse
from ...services.tempReserveService import (
    get_temp_reservation_by_id,
    create_temp_reservation,
    expire_temp_reservations,
    finalize_temp_reserevation
)
from ...db.session import get_db
from ...models.userModel import User
from ...utils.authUtil import get_current_user
from ...config import API_VERSION

router = APIRouter(prefix=f"{API_VERSION['v1']}/temp-reserve", tags=["Temp Reservation"])

@router.get("/{reservation_id}", response_model=TempReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return get_temp_reservation_by_id(reservation_id, db)

# Create a temporary reservation
@router.post("/new", response_model=TempReservationResponse)
def create_reservation(reservation_data: TempReservationCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_temp_reservation(db,user, reservation_data.event_id, reservation_data.seats_reserved)