from enum import Enum


class C3TestResultStatus(str, Enum):
    FAIL = "fail"
    PASS = "pass"
    SKIP = "skip"

    def __str__(self) -> str:
        return str(self.value)
