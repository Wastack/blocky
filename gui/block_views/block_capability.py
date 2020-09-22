from dataclasses import dataclass
from enum import Enum
from typing import Optional, FrozenSet


class WallType(Enum):
    SPIKE = 1


@dataclass
class BlockCapability:
    possible_wall_types: FrozenSet = frozenset()
    breaks_after: Optional[int] = None

