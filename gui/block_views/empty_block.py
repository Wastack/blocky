import tkinter
from typing import Optional, Any

from game.blocks.block import AbstractBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.utils.position import Position
from gui.block_views.block import BlockView


class EmptyBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas, block_fill_color="gray5")

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != EmptyBlock:
            return None
        return EmptyBlockView(canvas)

    def draw(self, pos: Position) -> Any:
        rect = super().draw(pos)
        return rect

    @staticmethod
    def repr() -> str:
        return "Empty block"

    def _set_default_block(self) -> AbstractBlock:
        return EmptyBlock()
