from enum import Enum


class MakeEnum(str, Enum):
    VALUE_0 = "48p-ethernet"
    VALUE_1 = "24p-ethernet"
    VALUE_2 = "24p-poe"
    VALUE_3 = "48p-poe"
    VALUE_4 = "32p-100g-ethernet"
    VALUE_5 = "48p-10g-4p-100g-ethernet"

    def __str__(self) -> str:
        return str(self.value)
