from game.blocks.block import AbstractBlock
from game.blocks.impl.rock import RockBlock
from game.gamemap import GameMap
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict


class RollableBlock(RockBlock):
    def __init__(self, game_map: GameMap):
        super().__init__()
        self._game_map = game_map

    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:
        # Let walls do their job
        super(RollableBlock, self).before_step(intruder, i)

        # Trying to roll
        self.move(i.direction)

    def move(self, direction) -> MoveVerdict:
        pass



