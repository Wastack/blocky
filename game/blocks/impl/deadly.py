from game.blocks.block import AbstractBlock
from game.blocks.impl.rock import RockBlock
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict


class DeadlyRockBlock(RockBlock):

    def before_step(self, intruder: AbstractBlock, _i : MoveInfo) -> MoveVerdict:

        # Try to kill it
        try:
            intruder.set_dead()
        except AttributeError:
            pass

        return MoveVerdict.NO_MOVE
