from dataclasses import dataclass
from typing import Optional, FrozenSet, Type

from gui.block_views.wall_views.wall_view import WallView


@dataclass
class BlockCapability:
    possible_wall_types: FrozenSet[Type[WallView]] = frozenset()
    breaks_after: Optional[int] = None

