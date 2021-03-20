from dataclasses import dataclass
from typing import Optional, FrozenSet, Type

from game.blocks.walls.wall import Wall


@dataclass
class BlockCapability:
    possible_wall_types: FrozenSet[Type[Wall]] = frozenset()
    breaks_after: Optional[int] = None

