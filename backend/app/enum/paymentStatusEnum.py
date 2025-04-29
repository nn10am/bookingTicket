from enum import Enum

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"