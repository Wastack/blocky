import logging

from game.blocks.block import AbstractBlock
from game.move_info import MoveInfo
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum
from game.utils.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.gamemap import GameMap
    from game.blocks.impl.stack import GameStack

dir_func_map = {
    Direction.DOWN: lambda pos: pos + Position(0, 1),
    Direction.UP: lambda pos: pos + Position(0, -1),
    Direction.RIGHT: lambda pos: pos + Position(1, 0),
    Direction.LEFT: lambda pos: pos + Position(-1, 0),
}


class Movable(AbstractBlock):
    def __init__(self):
        super().__init__()
        self._position = None
        self._game_map = None

    def initialize(self, pos: Position, game_map: 'GameMap'):
        self._position = pos
        self._game_map = game_map

    @property
    def position(self) -> Position:
        return self._position

    def move(self, d: Direction) -> MoveVerdict:
        """
        :param d: Direction the movable object takes
        :return: True, if state changed, false otherwise
        """
        if self._game_map is None:
            raise ValueError("Movable object is not initialized")
        elif self._position is None:
            # might be captured
            logging.warning("Movable tried to move without position set")
            return MoveVerdict(verdict=MoveVerdictEnum.INACTIVE)

        t = self._game_map.block(self._position).top()
        if type(t) != type(self):
            # I cannot find myself in game map
            raise ValueError(
                f"Cannot find movable object of type {type(self)} in position {self._position} Unexpected type: {type(t)}")

        move_info = MoveInfo(direction=d)
        new_pos = dir_func_map.get(d)(self._position)
        cell_to_interact = self._game_map.block(new_pos)
        result = cell_to_interact.before_step(self, move_info)
        cell_to_interact.after_step(self, move_info)

        if result.verdict == MoveVerdictEnum.MOVE:
            #logging.debug(f"Moving from {self._position} to {new_pos}")
            self._game_map.move(self._position, new_pos, self)
            self._position = new_pos
        elif result.verdict == MoveVerdictEnum.CAPTURED:
            # Movable is captured by something, remove from map
            self._game_map.block(self._position).pop()
            self._position = None

        return result

    def before_step(self, intruder: 'AbstractBlock', move_info: MoveInfo) -> MoveVerdict:
        return MoveVerdict(verdict=MoveVerdictEnum.NO_MOVE)

    def after_step(self, intruder: 'AbstractBlock', move_info: MoveInfo):
        return
