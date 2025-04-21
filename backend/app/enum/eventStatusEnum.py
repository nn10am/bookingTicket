from enum import Enum

class EventStatus(str, Enum):
    scheduled = "scheduled"
    postponed = "postponed"
    cancelled = "cancelled"
    completed = "completed"

    