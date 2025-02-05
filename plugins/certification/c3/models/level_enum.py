from enum import Enum


class LevelEnum(str, Enum):
    CERTIFIED = "Certified"
    CERTIFIED_PRE_INSTALL = "Certified Pre-Install"
    READY = "Ready"

    def __str__(self) -> str:
        return str(self.value)
