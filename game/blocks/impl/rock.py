from typing import Optional

from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class RockBlock(EmptyBlock):
    def __init__(self, walls: Optional[WallContainer] = None):
        self._walls = walls if walls is not None else WallContainer()

    def before_step(self, intruder: Moveable, i: MoveInfo) -> MoveVerdict:
        result = MoveVerdict.NO_MOVE
        walls_verdict = self._walls.before_step(intruder, i)
        return result if walls_verdict == MoveVerdict.NO_VERDICT else walls_verdict

    def after_step(self, intruder: Moveable, i: MoveInfo):
        self._walls.after_step(intruder, i)

