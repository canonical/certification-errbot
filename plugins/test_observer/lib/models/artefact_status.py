from enum import Enum


class ArtefactStatus(str, Enum):
    APPROVED = "APPROVED"
    MARKED_AS_FAILED = "MARKED_AS_FAILED"
    UNDECIDED = "UNDECIDED"

    def __str__(self) -> str:
        return str(self.value)
