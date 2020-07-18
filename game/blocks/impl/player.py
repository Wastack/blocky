from game.blocks.block import AbstractBlock
from game.moveables.moveable import Moveable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict


class Player(AbstractBlock, Moveable):
    def __init__(self, start_direction: Direction = Direction.DEFAULT):
        self._direction = start_direction
        self._dead = False

    @property
    def direction(self) -> Direction:
        return self._direction

    def set_direction(self, dir: Direction):
        self._direction = dir

    def before_step(self, intruder: Moveable) -> MoveVerdict:
        return MoveVerdict.NO_MOVE

    def after_step(self, intruder: Moveable):
        pass  # Empty block has no effect whatsoever

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    def is_alive(self) -> bool:
        return not self._dead
