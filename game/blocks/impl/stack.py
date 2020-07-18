from typing import List

from game.blocks.block import AbstractBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.impl.player import Player
from game.moveables.moveable import Moveable
from game.utils.move_verdict import MoveVerdict


class GameStack(AbstractBlock):
    def __init__(self):
        self._data: List[AbstractBlock] = [EmptyBlock()]

    def push(self, block: AbstractBlock):
        self._data.append(block)

    def pop(self) -> AbstractBlock:
        block = self._data.pop()
        if self._data == []:
            self._data.append(EmptyBlock())
        return block

    def top(self) -> AbstractBlock:
        return self._data[-1]

    def get_players(self) -> List[Player]:
        return [x for x in self._data if isinstance(x, Player)]

    def before_step(self, intruder: Moveable) -> MoveVerdict:
        """
        :return: Whether intruder can step on block
        """
        return MoveVerdict.MOVE if all(map(lambda x: x.before_step(intruder) != MoveVerdict.NO_MOVE, self._data))\
                                else MoveVerdict.NO_MOVE

    def after_step(self, intruder: Moveable) -> None:
        map(lambda x: x.after_step(), self._data)

