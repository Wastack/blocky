from typing import Optional

from game.blocks.block import AbstractBlock
from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class RockBlock(AbstractBlock):
    def __init__(self, walls: Optional[WallContainer] = None):
        self._walls = walls if walls is not None else WallContainer()

    def before_step(self, intruder: Moveable, i: MoveInfo) -> MoveVerdict:
        result = MoveVerdict.NO_MOVE
        walls_verdict = self._walls.before_step(intruder, i)
        return result if walls_verdict == MoveVerdict.NO_VERDICT else walls_verdict

    def after_step(self, intruder: Moveable, i: MoveInfo):
        self._walls.after_step(intruder, i)

    def wall_container(self) -> WallContainer:
        return self._walls

    def walls(self) -> Optional[WallContainer]:
        return self._walls
