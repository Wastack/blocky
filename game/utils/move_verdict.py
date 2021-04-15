from dataclasses import dataclass, field
from enum import Enum
from typing import List

from game.utils.MoveReports import MoveReport


class MoveVerdictEnum(Enum):
    MOVE = 0
    NO_MOVE = 1
    NO_VERDICT = 2
    CAPTURED = 3
    DELAYED = 4
    INACTIVE = 5


@dataclass
class MoveVerdict:
    verdict: MoveVerdictEnum
    reports: List[MoveReport] = field(default_factory=list)
