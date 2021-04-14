from enum import Enum


class MoveVerdict(Enum):
    MOVE = 0
    NO_MOVE = 1
    NO_VERDICT = 2
    CAPTURED = 3
    DELAYED = 4
    INACTIVE = 5
