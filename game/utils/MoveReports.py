from abc import ABC
from dataclasses import dataclass
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.utils.position import Position


# Class objects defined in this files are serialized by converting dataclasses
# to dicts. This means, serialized keys depend on variable name


@dataclass
class MoveReport(ABC):
    pass


@dataclass
class MeltingIceReport(MoveReport):
    life_was: int
    life_now: int
    position: 'Position'


@dataclass
class MovableMoveReport(MoveReport):
    position: 'Position'
    target: 'Optional[Position]'
    captured: bool = False


@dataclass
class PlayerMoveReport(MoveReport):
    position: 'Position'
    died: bool = False
