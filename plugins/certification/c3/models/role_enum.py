from enum import Enum


class RoleEnum(str, Enum):
    DUT = "DUT"
    SUPPORT = "Support"

    def __str__(self) -> str:
        return str(self.value)
