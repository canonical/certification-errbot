from enum import Enum


class StatusDeaEnum(str, Enum):
    DISPOSED_OF_OR_DESTROYED = "Disposed of or destroyed"
    IN_TRANSITSHIPPED = "In transit/Shipped"
    NOT_YET_SENT = "Not yet sent"
    OTHER = "Other"
    RETURNED_TO_PARTNERCUSTOMER = "Returned to partner/customer"
    UNKNOWN = "Unknown"
    WITH_CANONICAL = "With Canonical"

    def __str__(self) -> str:
        return str(self.value)
