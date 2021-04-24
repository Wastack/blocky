from game.move_info import MoveInfo
from game.moveables.movable import Movable
from game.utils.direction import Direction
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum

from typing import TYPE_CHECKING

from game.utils.position import Position

if TYPE_CHECKING:
    from game.blocks.block import AbstractBlock
    from game.gamemap import GameMap


class Player(Movable):
    def __init__(self, move_only_once: bool = False):
        super().__init__()

        # This decides whether Player wants to move only one, or until it is
        # stuck.
        self.__move_only_once = move_only_once

        # Turn id can be used to decide whether there is a new turn
        self.__turn_id = None

        # Inactive and momentum are defined in one turn. Should be reset for
        # each turn.
        self._inactive = False
        self._momentum = 0

        # Store whether player is already dead
        self._dead = False

        # Direction of Player to which it is facing
        self._facing = Direction.RIGHT

    def set_dead(self, is_dead=True):
        """
        Set whether player is dead or alive.
        :param is_dead:
        :return:
        """
        self._dead = is_dead

    @property
    def is_moving_only_once(self) -> bool:
        return self.__move_only_once

    @property
    def is_alive(self) -> bool:
        """
        :return: Whether player is alive
        """
        return not self._dead

    @property
    def is_active(self) -> bool:
        """
        :return: Whether player is still active in this *turn*.
                 e.g. if it hits a brick, it will no longer be active.
        """
        return not self._inactive

    @property
    def momentum(self) -> int:
        return self._momentum

    def set_active(self, active: bool = True) -> None:
        """
        Set whether player is active in current *turn*
        :param active:
        :return:
        """
        self._inactive = not active

    def set_facing(self, direction: Direction) -> None:
        """
        :param direction: New direction to which player is facing
        """
        self._facing = direction

    def before_step(self, intruder: 'AbstractBlock', i: MoveInfo) -> MoveVerdict:

        # When colliding with another player, that player should not stop,
        # because it might happen, that they move "simultaneously"
        return MoveVerdict(verdict=MoveVerdictEnum.DELAYED)

    @property
    def facing(self) -> Direction:
        return self._facing

    def move(self, d: Direction) -> MoveVerdict:
        """
        Executes a step of this player. If the player is already inactive, this
        won't cause any state changes in map.
        :param d: Direction the player should take
        :return: A verdict, which reflects the changes the move caused
        """
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

        # If player is capable to move only one step,
        # it should finish moving no matter what.
        if self.__move_only_once:
            self._inactive = True

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
