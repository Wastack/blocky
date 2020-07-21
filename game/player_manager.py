import logging

from game.blocks.impl.player import Player
from game.gamemap import GameMap
from game.move_info import MoveInfo
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict
from game.utils.position import Position

_dir_func_map = {
    Direction.DOWN : lambda pos: pos + Position(0, 1),
    Direction.UP: lambda pos: pos + Position(0, -1),
    Direction.RIGHT: lambda pos: pos + Position(1, 0),
    Direction.LEFT: lambda pos: pos + Position(-1, 0),
}



class PlayerManager:
    def __init__(self, map: GameMap):
        self._map = map

    def move_all_players(self, dir: Direction):
        player_info = [p for p in self._map.getPlayers() if p[0].is_alive()]
        logging.debug("Player info: {}".format(player_info))
        for player, pos in player_info:
            self.step_with(player, pos, dir)

    def step_with(self, p: Player, current_position: Position, dir: Direction):
        verdict = MoveVerdict.MOVE
        prev_pos = current_position
        move_info = MoveInfo(direction=dir, momentum=0)
        while verdict == MoveVerdict.MOVE:
            new_pos = _dir_func_map.get(dir)(prev_pos)
            cell_to_interact = self._map.block(new_pos)
            verdict = cell_to_interact.before_step(p, move_info)
            logging.debug(f"Can step verdict: {verdict} from pos: {new_pos}")
            if verdict == MoveVerdict.MOVE:
                logging.info(f"Player steps from: {prev_pos} to {new_pos}")
                self._map.move(prev_pos, new_pos, p)
            prev_pos = new_pos
            cell_to_interact.after_step(p, move_info)
            move_info.momentum += 1

