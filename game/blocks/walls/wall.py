from abc import ABC, abstractmethod
from typing import Optional

from game.move_info import MoveInfo
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.blocks.block import AbstractBlock


class Wall(ABC):
    @abstractmethod
    def before_step(self, intruder: 'AbstractBlock') -> MoveVerdict:
        return MoveVerdict(MoveVerdictEnum.NO_VERDICT)

    @abstractmethod
    def after_step(self, intruder: 'AbstractBlock') -> None:
        pass


class WallContainer():
    def __init__(self, left: Optional[Wall] = None, up: Optional[Wall] = None,
                 right: Optional[Wall] = None, down: Optional[Wall] = None):
        self._walls = {
            Direction.LEFT: left,
            Direction.UP: up,
            Direction.RIGHT: right,
            Direction.DOWN: down,
        }

    def walls(self):
        return self._walls

    def set_side(self, wall: Wall, side: Direction):
        self._walls[side] =  wall

    def before_step(self, intruder: 'AbstractBlock', i : MoveInfo) -> MoveVerdict:
        wall_side = Direction.opposite(i.direction)
        wall = self._walls.get(wall_side)
        if wall is None:
            return MoveVerdict(verdict=MoveVerdictEnum.NO_VERDICT)
        return self._walls[wall_side].before_step(intruder)

    def after_step(self, intruder: 'AbstractBlock', i: MoveInfo) -> None:
        wall_side = Direction.opposite(i.direction)
        return self._walls[wall_side].after_step(intruder)
