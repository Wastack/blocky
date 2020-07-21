from game.blocks.impl.rock import RockBlock
from game.moveables.moveable import Moveable


class Player(RockBlock, Moveable):
    def __init__(self):
        super().__init__()
        self._dead = False

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    def is_alive(self) -> bool:
        return not self._dead
