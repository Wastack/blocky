import tkinter
from typing import Optional, Any

from game.blocks.block import AbstractBlock
from game.blocks.impl.player import Player
from game.utils.position import Position
from gui.block_views.block import BlockView


class PlayerBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas, block_fill_color="gray5")
        self._text_id = None
        self._set_png_image("duck.png")

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != Player:
            return None

        ret = PlayerBlockView(canvas)
        ret._block = block
        return ret

    def draw(self, pos: Position) -> Any:
        self._set_png_image("frog.png" if self._block.is_moving_only_once else "duck.png")
        if self._text_id is not None:
            self.destroy()
        self._set_image_facing(self._block.facing)
        super().draw(pos)

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
