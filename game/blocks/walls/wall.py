from abc import ABC, abstractmethod
from typing import Optional

from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict


class Wall(ABC):
    @abstractmethod
    def before_step(self, intruder: Moveable) -> MoveVerdict:
        return MoveVerdict.NO_VERDICT

    @abstractmethod
    def after_step(self, intruder: Moveable) -> None:
        pass


class WallContainer():
    def __init__(self, left: Optional[Wall] = None, up: Optional[Wall] = None,
                 right: Optional[Wall] = None, down: Optional[Wall] = None):
        self._walls = {
            Direction.LEFT : left,
            Direction.UP: up,
            Direction.RIGHT: right,
            Direction.DOWN: down,
        }

    def before_step(self, intruder: Moveable, i : MoveInfo) -> MoveVerdict:
        wall_side = Direction.opposite(i.direction)
        wall = self._walls.get(wall_side)
        if wall is None:
            return MoveVerdict.NO_VERDICT
        return self._walls[wall_side].before_step(intruder)

    def after_step(self, intruder: Moveable, i: MoveInfo) -> None:
        wall_side = Direction.opposite(i.direction)
        return self._walls[wall_side].after_step(intruder)
