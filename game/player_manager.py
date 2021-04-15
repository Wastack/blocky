import random
from typing import Iterable, List

from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.gamemap import GameMap
from game.utils.MoveReports import MoveReport, PlayerMoveReport
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
    def move_all_players_one_step(direction: Direction, players_to_move: Iterable[Player]) -> List[MoveReport]:
        """
        This method executes one *step*.
        :param direction: Direction to which players move
        :param players_to_move: a collection of players that should be moved
        :return: Reports which were executed during this *step*
        """

        players = [p for p in players_to_move if p.is_alive and p.is_active]
        for p in players:
            p.set_active()

        reports: List[MoveReport] = []


        # Collect players that are unable to move *temporarly*, and move them
        # in the next loop.
        state_changed_in_loop = True
        while state_changed_in_loop:
            state_changed_in_loop = False
            delayed = []
            for p in players:
                result = p.move(direction)
                if result.verdict == MoveVerdictEnum.DELAYED:
                    delayed.append(p)  # Moving postponed
                else:
                    reports += result.reports

                if result.verdict == MoveVerdictEnum.MOVE:
                    state_changed_in_loop = True

            # Next loop with delayed players
            players = delayed

        return reports

    def execute_turn(self, direction: Direction) -> List[List[MoveReport]]:
        """
        Moves all players until they cannot move any longer.
        :param direction: Direction the players take
        """
        return list(self.execute_turn_yield_steps(direction))

    def execute_turn_yield_steps(self, direction: Direction) -> Iterable:
        """
        Executes one *turn*. Thus, players move until they cannot move any longer.
        Each *step* during execution is yielded.
        :param direction: Direction the players take
        """

        players = self._new_turn()

        reports = [None]  # None is hack for having a do while
        while len(reports) > 0:
            reports = self.move_all_players_one_step(direction, players)
            yield reports
