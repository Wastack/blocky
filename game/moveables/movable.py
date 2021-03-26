import logging

from game.blocks.impl.rock import RockBlock
from game.move_info import MoveInfo
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict
from game.utils.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.gamemap import GameMap

dir_func_map = {
    Direction.DOWN: lambda pos: pos + Position(0, 1),
    Direction.UP: lambda pos: pos + Position(0, -1),
    Direction.RIGHT: lambda pos: pos + Position(1, 0),
    Direction.LEFT: lambda pos: pos + Position(-1, 0),
}


class Movable(RockBlock):
    def __init__(self, pos: Position, game_map: 'GameMap'):
        super().__init__()
        self._position = pos
        self._game_map = game_map

    def move(self, d: Direction) -> bool:
        """
        :param d: Direction the movable object takes
        :return: True, if state changed, false otherwise
        """
        t = self._game_map.block(self._position).top()
        if type(t) != type(self):
            raise ValueError(
                f"Cannot find movable object of type {type(self)} in position {self._position} Unexpected type: {type(t)}")
        verdict = MoveVerdict.MOVE
        move_info = MoveInfo(direction=d, momentum=0)
        state_changed = False
        while verdict == MoveVerdict.MOVE:
            new_pos = dir_func_map.get(d)(self._position)
            cell_to_interact = self._game_map.block(new_pos)
            verdict = cell_to_interact.before_step(self, move_info)
            # logging.debug(f"Verdict of {new_pos} is {verdict}")

            if verdict != MoveVerdict.NO_MOVE:
                state_changed = True

            if verdict == MoveVerdict.MOVE:
                logging.debug(f"Moving from {self._position} to {new_pos}")
                self._game_map.move(self._position, new_pos, self)
                self._position = new_pos
            elif verdict == MoveVerdict.CAPTURED:
                # Movable is captured by something, remove from map
                self._game_map.block(self._position).pop()
            cell_to_interact.after_step(self, move_info)
            move_info.momentum += 1

        return state_changed
