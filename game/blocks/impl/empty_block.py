from game.blocks.block import AbstractBlock
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class EmptyBlock(AbstractBlock):

    def before_step(self, intruder: Moveable) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict.MOVE

    def after_step(self, intruder: Moveable):
        pass  # Empty block has no effect whatsoever
