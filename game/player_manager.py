from typing import List

from game.blocks.block import AbstractBlock
from game.gamemap import GameMap
from game.utils.direction import Direction

class PlayerManager:
    def __init__(self, game_map: GameMap):
        self._map = game_map

    def move_one(self, moveable: AbstractBlock, direction: Direction) -> bool:
        raise NotImplementedError()

    def move_all_players(self, direction: Direction) -> None:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """

        for p, position in self._map.getPlayers():
            if not p.is_alive():
                continue
            p.move(direction)
