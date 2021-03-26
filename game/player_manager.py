import logging

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


class PlayerManager:
    def __init__(self, game_map: GameMap):
        self._map = game_map

    def move_all_players(self, direction: Direction) -> None:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """

        # Ducks may prevent moving other duck. Make them move until there are
        # no more duck to move.
        state_changed = True
        while state_changed:
            player_info = [p for p in self._map.getPlayers() if p[0].is_alive()]
            state_changed = any([self.step_with(player, pos, direction) for player, pos in player_info])

    def step_with(self, p: Player, current_position: Position, direction: Direction) -> bool:
        """
        :param p: Player to move
        :param current_position:  Current position of player
        :param direction: Direction the player takes
        :return: False, if nothing changed. True otherwise.
        """
        is_state_changed = False
        verdict = MoveVerdict.MOVE

        prev_pos = current_position
        move_info = MoveInfo(direction=direction, momentum=0)
        while verdict == MoveVerdict.MOVE:
            new_pos = _dir_func_map.get(direction)(prev_pos)
            cell_to_interact = self._map.block(new_pos)
            verdict = cell_to_interact.before_step(p, move_info)
            if verdict != MoveVerdict.NO_MOVE:
                is_state_changed = True
            logging.debug(f"Verdict of {new_pos} is {verdict}")
            if verdict == MoveVerdict.MOVE:
                #logging.debug(f"Player steps from: {prev_pos} to {new_pos}")
                self._map.move(prev_pos, new_pos, p)
            elif verdict == MoveVerdict.CAPTURED:
                # Player is captured by something, remove from map
                # Assume player is on top of the stack
                if type(self._map.block(prev_pos).pop()) != Player:
                    raise ValueError("Captured player not found when trying to remove it")
                return True
            prev_pos = new_pos
            cell_to_interact.after_step(p, move_info)
            move_info.momentum += 1

        p.set_facing(direction)
        return is_state_changed
