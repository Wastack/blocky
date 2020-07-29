import tkinter
from typing import Optional, Any

from game.blocks.impl.rock import RockBlock
from game.utils.position import Position
from gui.block_views.block import BlockView


class RockBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas)
        self._text_id = None

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != RockBlock:
            return None
        return RockBlockView(canvas)

    def draw(self, pos: Position) -> Any:
        if self._text_id is not None:
            self.destroy()
        rect = super().draw(pos)
        self._text_id = self._create_text(pos, text="R")
        return rect

    def destroy(self):
        super().destroy()
        if self._text_id is not None:
            self._canvas.delete(self._text_id)
            self._text_id = None

    @staticmethod
    def repr() -> str:
        return "Stone"
