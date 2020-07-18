import logging
from typing import Iterable, Tuple, List

from game.blocks.block import AbstractBlock
from game.blocks.impl.deadly import DeadlyRockBlock
from game.blocks.impl.player import Player
from game.blocks.impl.stack import GameStack
from game.utils.game_error import GameError
from game.utils.position import Position
from game.utils.size import Size


class GameMap:

    def __init__(self, map_size: Size):
        self._map_size = map_size
        self._blocks: List[List[GameStack]] = []
        for w in range(self._map_size.width):
            column = []
            self._blocks.append(column)
            for h in range(self._map_size.height):
                column.append(GameStack())

    def block(self, pos: Position) -> AbstractBlock:
        if pos.x >= self._map_size.width or pos.x < 0 or \
                pos.y >= self._map_size.height or pos.y < 0:
            return DeadlyRockBlock()
        return self._blocks[pos.x][pos.y]

    def _block_as_stack(self, pos: Position) -> GameStack:
        if pos.x >= self._map_size.width or pos.x < 0 or \
                pos.y >= self._map_size.height or pos.y < 0:
            raise GameError("Index out of bounds")
        return self._blocks[pos.x][pos.y]

    def getPlayers(self) -> [Iterable[Tuple[Player, Position]]]:
        result = [(b, Position(w, h)) for w, row in enumerate(self._blocks) for h, s in enumerate(row) for b in s.get_players()]
        return result

    def putBlock(self, pos: Position, block: AbstractBlock):
        self._block_as_stack(pos).push(block)

    def move(self, pos_from: Position, pos_to: Position, what: AbstractBlock):
        cell = self._block_as_stack(pos_from)
        if cell.top() != what:
            raise GameError('Block should be a stack object. PutBlock target might be out of bounds.')
        self.putBlock(pos_to, cell.pop())

