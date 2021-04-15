from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.blocks.walls.wall import Wall
from game.utils.MoveReports import PlayerMoveReport
from game.utils.move_verdict import MoveVerdict, MoveVerdictEnum


class KillerWall(Wall):
    def before_step(self, intruder: AbstractBlock) -> MoveVerdict:
        verdict = MoveVerdict(verdict=MoveVerdictEnum.NO_MOVE)
        try:
            intruder: Player
            intruder.set_dead()
            verdict.reports.append(PlayerMoveReport(
                pos_was=intruder.position, pos_now=None, died=True))
        except AttributeError:
            pass  # Intruder is not player
        return verdict

    def after_step(self, intruder: AbstractBlock) -> None:
        return
