import tkinter
from typing import Optional, Any

from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.utils.position import Position
from gui.block_views.block import BlockView


class PlayerBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas)
        self._text_id = None

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != Player:
            return None

        ret = PlayerBlockView(canvas)
        ret._block = block
        return ret

    def draw(self, pos: Position) -> Any:
        if self._text_id is not None:
            self.destroy()
        super().draw(pos)

        text = ":)" if self._block.is_alive() else "X("
        self._text_id = self._create_text(pos, text=text)

    def destroy(self):
        super().destroy()
        if self._text_id is not None:
            self._canvas.delete(self._text_id)
            self._text_id = None

    @staticmethod
    def repr() -> str:
        return "Player"

    def _set_default_block(self) -> AbstractBlock:
        return Player()
