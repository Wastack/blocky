from dataclasses import dataclass
from typing import Optional

from game.utils.direction import Direction
from game.utils.position import Position


@dataclass
class MoveInfo:
    direction: Direction = Direction.DEFAULT
    target: Optional[Position] = None

