from enum import Enum


class TestExecutionsPatchRequestStatusType1(str, Enum):
    COMPLETED = "COMPLETED"

    def __str__(self) -> str:
        return str(self.value)
