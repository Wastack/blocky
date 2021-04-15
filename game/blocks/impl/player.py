import logging

from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.blocks.block import AbstractBlock


class Player(Movable):
    def __init__(self):
        super().__init__()

        # Turn id can be used to decide whether there is a new turn
        self.__turn_id = None

        # Inactive and momentum are defined in one turn. Should be resetted for
        # each turn
        self._inactive = False
        self._momentum = 0


        self._dead = False
        self._facing = Direction.RIGHT

    def set_dead(self, is_dead=True):
        self._dead = is_dead

    @property
    def is_alive(self) -> bool:
        return not self._dead

    @property
    def is_active(self) -> bool:
        return not self._inactive

    @property
    def momentum(self) -> int:
        return self._momentum


    def set_active(self, active: bool = True) -> None:
        self._inactive = not active


    def set_facing(self, direction: Direction):
        self._facing = direction

    def before_step(self, intruder: 'AbstractBlock', i: MoveInfo) -> MoveVerdict:

        # When colliding with another player, that player should not stop,
        # because it might happen, that they move "simultaneously"
        return MoveVerdict(verdict=MoveVerdictEnum.DELAYED)

    @property
    def facing(self) -> Direction:
        return self._facing

    def move(self, d: Direction) -> MoveVerdict:
        if self._inactive:
            return MoveVerdict(verdict=MoveVerdictEnum.INACTIVE)

        verdict = super(Player, self).move(d)

        if verdict.verdict == MoveVerdictEnum.NO_MOVE or verdict.verdict == MoveVerdictEnum.CAPTURED:
            self._inactive = True
        elif verdict.verdict == MoveVerdictEnum.NO_VERDICT:
            raise RuntimeError("Inconclusive verdict when trying to move")
        elif verdict.verdict == MoveVerdictEnum.MOVE:
            self._momentum += 1

        self.set_facing(d)

        return verdict

    def reset_turn(self, turn_id: int) -> None:
        """
        Start a new turn. It also resets properties from previous turn.
        :param turn_id: turn identifier
        :return:
        """
        self.__turn_id = turn_id
        self._inactive = False
        self._momentum = 0
