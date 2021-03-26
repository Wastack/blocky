from game.blocks.impl.rock import RockBlock
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class DeadlyRockBlock(RockBlock):

    def before_step(self, intruder: Moveable, _i : MoveInfo) -> MoveVerdict:
        intruder.set_dead()
        return MoveVerdict.NO_MOVE
