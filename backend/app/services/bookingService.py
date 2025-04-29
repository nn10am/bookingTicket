from sqlalchemy.orm import Session
from ..models import Booking, Event, User 
from fastapi import HTTPException, status
from .userService import get_user_by_id
from .eventService import fetch_event_by_id
from ..utils.errorHandleUtil import not_found_error, insufficient_seat

