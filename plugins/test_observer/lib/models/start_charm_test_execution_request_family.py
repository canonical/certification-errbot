from enum import Enum


class StartCharmTestExecutionRequestFamily(str, Enum):
    CHARM = "charm"

    def __str__(self) -> str:
        return str(self.value)
