from enum import Enum


class StartDebTestExecutionRequestExecutionStage(str, Enum):
    PROPOSED = "proposed"
    UPDATES = "updates"

    def __str__(self) -> str:
        return str(self.value)
