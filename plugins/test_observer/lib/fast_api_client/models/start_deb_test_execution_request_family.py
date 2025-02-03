from enum import Enum


class StartDebTestExecutionRequestFamily(str, Enum):
    DEB = "deb"

    def __str__(self) -> str:
        return str(self.value)
