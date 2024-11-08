from enum import Enum

class Status(Enum):
    PENDING = "PENDING"
    ORDERED = "ORDERED"
    def __str__(self):
        return self.value