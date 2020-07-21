from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class EmptyBlock(AbstractBlock):

    def before_step(self, intruder: Moveable, _i: MoveInfo) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict.MOVE

    def after_step(self, intruder: Moveable, _i: MoveInfo):
        pass  # Empty block has no effect whatsoever
