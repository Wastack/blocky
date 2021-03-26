from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict
from game.utils.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.gamemap import GameMap


class Player(Movable):
    def __init__(self):
        super().__init__(None, None)
        self._dead = False
        self._facing = Direction.RIGHT

    def initialize(self, position: Position, game_map: 'GameMap'):
        super().__init__(pos=position, game_map=game_map)

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    def is_alive(self) -> bool:
        return not self._dead

    def set_facing(self, direction: Direction):
        self._facing = direction

    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:
        if self._position is None:
            raise ValueError("Player is not initialized")

        if type(intruder) == Player:
            # Start moving, so the other duck can finish its moving as well
            state_changed = self.move(i.direction)
            if state_changed:
                return MoveVerdict.MOVE  # We went out of the way
            else:
                return MoveVerdict.NO_MOVE # Cannot move out of the way

    @property
    def facing(self) -> Direction:
        return self._facing

    def move(self, d: Direction) -> bool:
        if self._position is None:
            raise ValueError("Player is not initialized")

        state_changed = super(Player, self).move(d)
        self.set_facing(d)
        return state_changed
