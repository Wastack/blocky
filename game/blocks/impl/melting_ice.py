from typing import Optional

from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.blocks.impl.rock import RockBlock
from game.blocks.walls.wall import WallContainer
from game.move_info import MoveInfo
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class MeltingIceBlock(RockBlock):
    """
    A block which behaves similarly to Rock block, only it disappears after being hit 'life' times.
    """

    def __init__(self, walls: Optional[WallContainer] = None, life: int = 1):
        """
        :param walls: Walls on the melting ice block
        :param life: Defines how many times the block can be hit before disappearing --
                     i.e. before being a simple empty block.
        """

        super().__init__(walls)
        if life < 1:
            raise ValueError("Life parameter of melting ice block should be at least 1 when creating")
        self._life = life

    @property
    def life(self) -> int:
        return self._life

    def set_life(self, life: int):
        if life < 1:
            raise ValueError("Life parameter of ice block should be at least 1")
        self._life = life

    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:
        if self._life > 0:
            # Ice only melts if intruder comes from a distance
            if i.momentum > 0 and isinstance(intruder, Player):
                self._life -= 1
            return super(MeltingIceBlock, self).before_step(intruder, i)
        return MoveVerdict.MOVE
