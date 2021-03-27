from typing import List, Iterable

from game.blocks.block import AbstractBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.impl.player import Player
from game.move_info import MoveInfo
from game.utils.move_verdict import MoveVerdict


class GameStack(AbstractBlock):
    def __init__(self):
        self._data: List[AbstractBlock] = []

    def push(self, block: AbstractBlock):
        if isinstance(block, EmptyBlock):
            return
        self._data.append(block)

    def pop(self) -> AbstractBlock:
        if self._data == []:
            return EmptyBlock()
        block = self._data.pop()
        return block

    def top(self) -> AbstractBlock:
        if not self._data:
            return EmptyBlock()
        return self._data[-1]

    def data(self) -> List[AbstractBlock]:
        return self._data[:]

    def get_players(self) -> Iterable[Player]:
        return (x for x in self._data if isinstance(x, Player))

    def clear(self):
        self._data.clear()

    def before_step(self, intruder: AbstractBlock, i: MoveInfo) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        if self._data == []:
            return MoveVerdict.MOVE
        top_verdict = self.top().before_step(intruder, i)
        return top_verdict

    def after_step(self, intruder: AbstractBlock, i: MoveInfo) -> None:
        map(lambda x: x.after_step(intruder, i), self._data)
