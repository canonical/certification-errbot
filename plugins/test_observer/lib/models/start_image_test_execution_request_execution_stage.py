from enum import Enum


class StartImageTestExecutionRequestExecutionStage(str, Enum):
    CURRENT = "current"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
