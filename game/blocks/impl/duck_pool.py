from typing import Optional

from game.blocks.block import AbstractBlock
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

    def __init__(self, walls: Optional[WallContainer] = None, capacity: int = -1):
        """
        :param walls: Walls on the pool.
        :param capacity: Defines how many blocks the pool can accept. -1 means infinite capacity
        """

        super().__init__(walls)
        if capacity < -1:
            raise ValueError("Invalid capacity")
        self._capacity = capacity
        self._blocks_in_pool = []  # This might needed later for pretty rendering. (e.g. ducks floating in the pool)

    @property
    def free_space(self) -> int:
        if self._capacity == -1:
            return -1
        return self._capacity - len(self._blocks_in_pool)

    @property
    def capacity(self) -> int:
        return self._capacity

    def set_capacity(self, capacity: int):
        self._capacity = capacity

    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:
        walls_verdict = self._walls.before_step(intruder, i)
        if walls_verdict != MoveVerdict.NO_VERDICT:
            return walls_verdict

        if self.free_space > 0 or self._capacity == -1:
            # Accept block
            self._blocks_in_pool.append(intruder)
            return MoveVerdict.CAPTURED

        # If full, behaves like a rock
        return super(DuckPoolBlock, self).before_step(intruder, i)

