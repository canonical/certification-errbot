from enum import Enum


class StartSnapTestExecutionRequestFamily(str, Enum):
    SNAP = "snap"

    def __str__(self) -> str:
        return str(self.value)
