from enum import Enum


class ComponentReleaseStatusStatusEnum(str, Enum):
    CERTIFIED = "certified"
    INPROGRESS = "inprogress"
    UNSUPPORTED = "unsupported"

    def __str__(self) -> str:
        return str(self.value)
