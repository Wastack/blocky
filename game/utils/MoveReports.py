from abc import ABC
from dataclasses import dataclass
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.utils.position import Position


@dataclass
class MoveReport(ABC):
    pass


@dataclass
class MeltingIceReport(MoveReport):
    life_was: int
    life_now: int


@dataclass
class MovableMoveReport(MoveReport):
    pos_was: 'Position'
    pos_now: 'Optional[Position]'
    captured: bool = False


@dataclass
class PlayerMoveReport(MovableMoveReport):
    died: bool = False
