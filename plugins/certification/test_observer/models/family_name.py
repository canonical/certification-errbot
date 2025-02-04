from enum import Enum


class FamilyName(str, Enum):
    CHARM = "charm"
    DEB = "deb"
    IMAGE = "image"
    SNAP = "snap"

    def __str__(self) -> str:
        return str(self.value)
