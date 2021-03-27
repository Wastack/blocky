import logging

from game.blocks.impl.melting_ice import MeltingIceBlock
from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict
from game.utils.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.gamemap import GameMap
    from game.blocks.block import AbstractBlock
    from game.blocks.impl.stack import GameStack


class Player(Movable):
    def __init__(self):
        super().__init__(None, None)
        self.__turn_id = None
        self.__i_wont_move_in_this_turn = -1
        self._dead = False
        self._facing = Direction.RIGHT

    def initialize(self, position: Position, game_map: 'GameMap'):
        super().__init__(pos=position, game_map=game_map)

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    @property
    def is_alive(self) -> bool:
        return not self._dead

    def set_facing(self, direction: Direction):
        self._facing = direction

    def before_step(self, intruder: 'AbstractBlock', i: MoveInfo) -> MoveVerdict:
        if self._position is None:
            raise ValueError("Player is not initialized")

        if type(intruder) == Player:
            # Start moving, so the other duck can finish its moving as well
            state_changed = self.move(i.direction)
            if state_changed:
                return MoveVerdict.MOVE  # We went out of the way
            else:
                return MoveVerdict.NO_MOVE  # Cannot move out of the way

    @property
    def facing(self) -> Direction:
        return self._facing

    def move(self, d: Direction) -> bool:
        if self._position is None:
            raise ValueError("Player is not initialized")

        state_changed = super(Player, self).move(d)
        self.set_facing(d)
        return state_changed

    def _before_moving(self, target_cell: 'GameStack', move_info: MoveInfo) -> bool:
        if self.__turn_id == self.__i_wont_move_in_this_turn:
            return False
        top = target_cell.top()
        if isinstance(top, MeltingIceBlock) and top.life == 1:
            # We need to make sure that this duck cannot be pushed into
            # the place of the recently (about to be) melted ice.
            logging.info(f"Duck melted ice in pos: {self.position}. Further move for duck is forbidden")
            self.__i_wont_move_in_this_turn = self.__turn_id
        return True

    def set_turn_id(self, turn_id: int) -> None:
        self.__turn_id = turn_id
