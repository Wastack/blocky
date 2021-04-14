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
        self_move_verdict = self.move(i.direction)
        if self_move_verdict == MoveVerdict.MOVE or \
                self_move_verdict == MoveVerdict.CAPTURED:
            logging.debug("I am no longer in the way")
            # I was able to move out from the way
            return MoveVerdict.MOVE
        elif self_move_verdict == MoveVerdict.DELAYED:
            return self_move_verdict
        else:
            logging.debug("I could NOT move")
            # Cannot move out ot the way
            return super(Boulder, self).before_step(intruder, i)
