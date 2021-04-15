from game.blocks.block import AbstractBlock
from game.blocks.impl.rock import RockBlock
from game.move_info import MoveInfo
from game.utils.MoveReports import PlayerMoveReport
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.blocks.impl.player import Player


class DeadlyRockBlock(RockBlock):

    def before_step(self, intruder: AbstractBlock, _i: MoveInfo) -> MoveVerdict:
        verdict = MoveVerdict(verdict=MoveVerdictEnum.NO_MOVE)

        # Try to kill it
        try:
            intruder: 'Player'
            intruder.set_dead()
            verdict.reports.append(PlayerMoveReport(
                position=intruder.position, died=True))
        except AttributeError:
            pass

        return verdict
