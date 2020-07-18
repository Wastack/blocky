from game.blocks.impl.empty_block import EmptyBlock
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class DeadlyRockBlock(EmptyBlock):

    def before_step(self, intruder: Moveable) -> MoveVerdict:
        intruder.set_dead()
        return MoveVerdict.NO_MOVE
