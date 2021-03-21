
from game.blocks.impl.rock import RockBlock
from game.moveables.moveable import Moveable
from game.utils.direction import Direction


class Player(RockBlock, Moveable):
    def __init__(self):
        super().__init__()
        self._dead = False
        self._facing = Direction.RIGHT

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    def is_alive(self) -> bool:
        return not self._dead

    def set_facing(self, direction: Direction):
        self._facing = direction

    @property
    def facing(self) -> Direction:
        return self._facing
