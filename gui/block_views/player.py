import tkinter
from typing import Optional, Any

from game.blocks.impl.player import Player
from game.utils.position import Position
from gui.block_views.block import BlockView


class PlayerBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas)

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != Player:
            return None
        return PlayerBlockView(canvas)

    def draw(self, pos: Position) -> Any:
        rect = super().draw(pos)
        self._create_text(pos, text="P")
        return rect

    @staticmethod
    def repr() -> str:
        return "Player"
