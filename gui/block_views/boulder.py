import tkinter
from typing import Optional, Any

from game.blocks.block import AbstractBlock
from game.blocks.impl.boulder import Boulder
from gui.block_views.block import BlockView


class BoulderView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas, block_fill_color="gray5")
        self._png_file_name = "boulder.png"

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != Boulder:
            return None
        return BoulderView(canvas)

    @staticmethod
    def repr() -> str:
        return "RollingBlock"

    def _set_default_block(self) -> AbstractBlock:
        return Boulder()
