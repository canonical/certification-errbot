from enum import Enum


class TestExecutionStatus(str, Enum):
    ENDED_PREMATURELY = "ENDED_PREMATURELY"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    NOT_STARTED = "NOT_STARTED"
    NOT_TESTED = "NOT_TESTED"
    PASSED = "PASSED"

    def __str__(self) -> str:
        return str(self.value)
