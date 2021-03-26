from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.blocks.walls.wall import Wall
from game.utils.move_verdict import MoveVerdict


class KillerWall(Wall):
    def before_step(self, intruder: AbstractBlock) -> MoveVerdict:
        if isinstance(intruder, Player):
            intruder.set_dead()
        return MoveVerdict.NO_MOVE

    def after_step(self, intruder: AbstractBlock) -> None:
        return
