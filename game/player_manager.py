import logging
from dataclasses import dataclass
from typing import List

from game.blocks.impl.player import Player
from game.gamemap import GameMap
from game.move_info import MoveInfo
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict
from game.utils.position import Position

_dir_func_map = {
    Direction.DOWN: lambda pos: pos + Position(0, 1),
    Direction.UP: lambda pos: pos + Position(0, -1),
    Direction.RIGHT: lambda pos: pos + Position(1, 0),
    Direction.LEFT: lambda pos: pos + Position(-1, 0),
}

class _PlayerWithPosition:
    def __init__(self, player: Player, pos: Position, game_map: GameMap):
        self._player = player
        self._position = pos
        self._map = game_map

        self._definitely_done_moving = False

    def step_with(self, direction: Direction) -> bool:
        """
        :param direction: Direction the player takes
        :return: True, if state changed, false otherwise
        """
        if self._definitely_done_moving:
            return False

        verdict = MoveVerdict.MOVE
        prev_pos = self._position
        move_info = MoveInfo(direction=direction, momentum=0)
        state_changed = False
        while verdict == MoveVerdict.MOVE:
            new_pos = _dir_func_map.get(direction)(prev_pos)
            cell_to_interact = self._map.block(new_pos)
            verdict = cell_to_interact.before_step(self._player, move_info)
            #logging.debug(f"Verdict of {new_pos} is {verdict}")

            if verdict != MoveVerdict.NO_MOVE:
                state_changed = True

            if verdict == MoveVerdict.NO_MOVE and isinstance(cell_to_interact.top(), Player):
                self._done_moving = False
            elif verdict == MoveVerdict.NO_MOVE:
                self._definitely_done_moving = True
            elif verdict == MoveVerdict.MOVE:
                logging.debug(f"Moving from {self._position} to {new_pos}")
                self._map.move(prev_pos, new_pos, self._player)
                self._position = new_pos
            elif verdict == MoveVerdict.CAPTURED:
                # Player is captured by something, remove from map
                # Assume player is on top of the stack
                if type(self._map.block(prev_pos).pop()) != Player:
                    raise ValueError("Captured player not found when trying to remove it")
                self._definitely_done_moving = True
            prev_pos = new_pos
            cell_to_interact.after_step(self._player, move_info)
            move_info.momentum += 1

        self._player.set_facing(direction)
        return state_changed

class PlayerManager:
    def __init__(self, game_map: GameMap):
        self._map = game_map

    def move_all_players(self, direction: Direction) -> None:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """

        players: List[_PlayerWithPosition] = []
        for p, position in self._map.getPlayers():
            if not p.is_alive():
                continue
            players.append(_PlayerWithPosition(player=p, pos=position, game_map=self._map))

        # Ducks may prevent moving other duck. Make them move until there are
        # no more duck to move.
        state_changed = True
        while state_changed:
            state_changed = any([x.step_with(direction) for x in players])
