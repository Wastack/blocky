from abc import ABC, abstractmethod
from typing import List, Optional

from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class AbstractBlock(ABC):
    def walls(self) -> Optional[WallContainer]:
        return None

    @abstractmethod
    def before_step(self, intruder: Moveable, move_info: MoveInfo) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict.NO_VERDICT

    @abstractmethod
    def after_step(self, intruder: Moveable, move_info: MoveInfo):
        return True
