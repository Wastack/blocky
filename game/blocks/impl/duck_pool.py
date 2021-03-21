from typing import Optional

from game.blocks.impl.player import Player
from game.blocks.impl.rock import RockBlock
from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class DuckPoolBlock(RockBlock):
    """
    The player blocks (ducks) need to reach the duck pool blocks.
    If pool is full, it behaves as a rock
    """

    def __init__(self, walls: Optional[WallContainer] = None, capacity: int = 0):
        """
        :param walls: Walls on the pool.
        :param capacity: Defines how many blocks the pool can accept. 0 means infinite capacity
        """

        super().__init__(walls)
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self._capacity = capacity
        self._blocks_in_pool = []  # This might needed later for pretty rendering. (e.g. ducks floating in the pool)

    @property
    def free_space(self) -> int:
        return self._capacity - len(self._blocks_in_pool)

    @property
    def capacity(self) -> int:
        return self._capacity

    def before_step(self, intruder: Moveable, i: MoveInfo) -> MoveVerdict:
        walls_verdict = self._walls.before_step(intruder, i)
        if walls_verdict != MoveVerdict.NO_VERDICT:
            return walls_verdict

        if self.free_space > 0 or self._capacity == 0:
            # Accept block
            self._blocks_in_pool.append(intruder)
            return MoveVerdict.CAPTURED

        # If full, behaves like a rock
        return super(DuckPoolBlock, self).before_step(intruder, i)

