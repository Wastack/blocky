import random

from game.blocks.block import AbstractBlock
from game.gamemap import GameMap
from game.utils.direction import Direction


class PlayerManager:
    _ID_BIT_NUM = 128

    def __init__(self, game_map: GameMap):
        self._map = game_map
        self.__reset_id()

    def __reset_id(self):
        self._turn_id = random.getrandbits(PlayerManager._ID_BIT_NUM)

    @property
    def turn_id(self) -> int:
        return self._turn_id

    def move_one(self, moveable: AbstractBlock, direction: Direction) -> bool:
        raise NotImplementedError()

    def move_all_players(self, direction: Direction) -> None:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """

        self.__reset_id()
        players = list(self._map.getPlayers())

        # Set turn ID on players
        for p in players:
            p.set_turn_id(self.turn_id)

        # Start moving players
        for p in (x for x in players if x.is_alive):
            p.move(direction)
