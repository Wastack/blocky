import random
from typing import Iterable

from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.gamemap import GameMap
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdictEnum


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

    def _new_turn(self) -> Iterable[Player]:
        self.__reset_id()
        players = list(self._map.getPlayers())

        # Set turn ID on players
        for p in players:
            p.reset_turn(self.turn_id)

        return players

    def move_one_player(self, moveable: AbstractBlock, direction: Direction) -> bool:
        raise NotImplementedError()

    @staticmethod
    def move_all_players_one_step(direction: Direction, players_to_move: Iterable[Player]) -> bool:
        """
        :param direction: Direction to which players move
        :param players_to_move: a collection of players that should be moved
        :return: True if there is a change and so the turn is not over. False otherwise.
        """

        players = [p for p in players_to_move if p.is_alive and p.is_active]
        for p in players:
            p.set_active()

        state_changed_overall = False

        state_changed_in_loop = True
        while state_changed_in_loop:
            state_changed_in_loop = False
            delayed = []
            for p in players:
                result = p.move(direction)
                if result.verdict == MoveVerdictEnum.DELAYED:
                    delayed.append(p)  # Moving postponed
                elif result.verdict == MoveVerdictEnum.MOVE:
                    state_changed_overall = True
                    state_changed_in_loop = True

            # Next loop with delayed players
            players = delayed

        # TODO also return movement infos
        return state_changed_overall

    def move_all_players(self, direction: Direction) -> None:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """

        players = self._new_turn()

        state_changed = True
        while state_changed:
            state_changed = self.move_all_players_one_step(direction, players)
            # TODO yield movement info
