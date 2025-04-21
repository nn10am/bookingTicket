from fastapi import HTTPException, status
from ..enum.userEnum import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH, PASSWORD_MIN_LENGTH
from ..enum.eventStatusEnum import EventStatus
# User already exists 
def user_exists_error(field: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{field} already exists."
    )

# Invalid user data
def invalid_data_error(message: str):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )

# Username length limit
def validate_username_length(username: str):
    if len(username) > USERNAME_MAX_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Username must not exceed {USERNAME_MAX_LENGTH} characters."
        )

# Email length limit
def validate_email_length(email: str):
    if len(email) > EMAIL_MAX_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Email must not exceed {EMAIL_MAX_LENGTH} characters."
        )
    
# Password length limit
def validate_password_length(password: str):
    if len(password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Password must be at least {PASSWORD_MIN_LENGTH} characters long."
        )
    
# Generic error
def generic_error():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Something went wrong during registration."
    )

# Incorrect username or password
def login_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Incorrect username or password. Please try again."
    )

# Total seats value error
def seats_negative_error():
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Number of seats cannot be negative."
    )

# Available seats value exceeds total seats value
def available_seats_exceed_error():
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Avaialbe seats cannot exceed total seats."
    )

# Not found error
def not_found_error(entity: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} not found"
    )

# Event status error
def invalid_event_status_error():
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Invalid event status"
    )

# Validate event status
def validate_event_status(status: str):
    if status not in EventStatus:
        invalid_event_status_error()

# Transition of event status error
def invalid_eventStatus_transition_error(current_status: str, new_status: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            f"Invalid event status transition: cannot change event status "
            f"from '{current_status}' to '{new_status}'."
        )
    )

# Invalid event status transition
def validate_eventStatus_transition(current_status: str, new_status: str):
    transitions = {
        "scheduled": {"scheduled","postponed", "cancelled", "completed"},
        "postponed": {"scheduled", "cancelled", "postponed"},
        "cancelled": set(), # no changes allowed
        "completed": set(), # no changes allowed
    }

    if new_status not in transitions.get(current_status, set()):
        invalid_eventStatus_transition_error(current_status, new_status)

# Restricted filed edit
def restricted_field_edit_error(field: str, reason: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Cannot update '{field}': {reason}"
    )