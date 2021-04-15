from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum


class EmptyBlock(AbstractBlock):

    def before_step(self, intruder: AbstractBlock, _i: MoveInfo) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict(verdict=MoveVerdictEnum.MOVE)

    def after_step(self, intruder: AbstractBlock, _i: MoveInfo):
        pass  # Empty block has no effect whatsoever
