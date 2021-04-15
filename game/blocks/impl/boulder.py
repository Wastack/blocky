import logging

from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum


class Boulder(Movable):
    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:

        # Another block of this type cannot push
        if isinstance(intruder, Boulder):
            return MoveVerdict(verdict=MoveVerdictEnum.NO_MOVE)

        # Trying to roll
        result = self.move(i.direction)
        if result.verdict == MoveVerdictEnum.CAPTURED:
            logging.debug("Boulder captured, cell is free now")
            # I was able to move out from the way
            result.verdict = MoveVerdictEnum.MOVE

        return result
