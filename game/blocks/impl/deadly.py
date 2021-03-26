from game.blocks.block import AbstractBlock
from game.blocks.impl.rock import RockBlock
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict


class DeadlyRockBlock(RockBlock):

    def before_step(self, intruder: AbstractBlock, _i : MoveInfo) -> MoveVerdict:
        intruder.set_dead()
        return MoveVerdict.NO_MOVE
