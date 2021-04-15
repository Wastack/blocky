from dataclasses import dataclass
from game.utils.direction import Direction


@dataclass
class MoveInfo:
    direction: Direction = Direction.DEFAULT

