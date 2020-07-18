from abc import ABC, abstractmethod

from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class AbstractBlock(ABC):

    @abstractmethod
    def before_step(self, intruder: Moveable) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict.NO_VERDICT

    @abstractmethod
    def after_step(self, intruder: Moveable):
        return True

