from abc import ABC, abstractmethod
from typing import Optional

from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum


class AbstractBlock(ABC):
    def walls(self) -> Optional[WallContainer]:
        return None

    @abstractmethod
    def before_step(self, intruder: 'AbstractBlock', move_info: MoveInfo) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict(verdict=MoveVerdictEnum.NO_VERDICT)

    @abstractmethod
    def after_step(self, intruder: 'AbstractBlock', move_info: MoveInfo):
        return True
