import logging

from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.move_verdict import MoveVerdict


class Boulder(Movable):
    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:

        # Another block of this type cannot push
        if isinstance(intruder, Boulder):
            return MoveVerdict.NO_MOVE

        # Trying to roll
        if self.move(i.direction):
            logging.debug("I could move")
            # I was able to move out from the way
            return MoveVerdict.MOVE
        else:
            logging.debug("I could NOT move")
            # Cannot move out ot the way
            return super(Boulder, self).before_step(intruder, i)

    def _before_moving(self, target_cell, move_info) -> bool:
        return True
