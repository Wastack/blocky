import tkinter
from typing import Optional, Any, List

from game.blocks.block import AbstractBlock
from game.blocks.impl.duck_pool import DuckPoolBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.blocks.walls.killer_wall import KillerWall
from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block import BlockView
from gui.block_views.block_capability import BlockCapability
from gui.block_views.wall_views import wall_factory
from gui.block_views.wall_views.wall_view import WallView


class DuckPoolBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas, block_fill_color="gray5")
        self._text_id = None
        self._wall_views: List[WallView] = []
        self._set_png_image("duck_pool.png")

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block: MeltingIceBlock) -> Optional['BlockView']:
        if type(block) != DuckPoolBlock:
            return None

        rock_view = DuckPoolBlockView(canvas)
        rock_view._block = block
        return rock_view

    def draw(self, pos: Position) -> Any:
        if self._text_id is not None:
            self.destroy()

        if self._block.capacity < 0:
            pass  # TODO WHAT

        captured_count = self._block.captured_count
        if captured_count > 0:
            draw_count = 3 if captured_count > 2 else captured_count
            self._png_file_name = f"duck_pool_{draw_count}_duck.png"

        rect = super().draw(pos)

        if self._block.capacity > -1:
            self._text_id = self._create_text(pos, text=f"{self._block.free_space}")

        # Draw walls
        wall_container = self._block.walls()
        if wall_container:
            for side, wall in wall_container.walls().items():
                if wall is None:
                    continue
                self._wall_views.append(wall_factory.from_wall(
                    wall, side, self._canvas))

        for wv in self._wall_views:
            wv.draw(pos)

        return rect

    def destroy(self):
        super().destroy()
        for w in self._wall_views:
            if w is None:
                continue
            w.destroy()
        self._wall_views.clear()

        if self._text_id is not None:
            self._canvas.delete(self._text_id)
            self._text_id = None

    @staticmethod
    def repr() -> str:
        return "DuckPool"

    @staticmethod
    def block_capability() -> BlockCapability:
        return BlockCapability(possible_wall_types=frozenset([KillerWall]))

    def set_wall(self, side: Direction, wall: Optional[Wall]):
        self._block.walls().set_side(wall, side)

    def _set_default_block(self) -> AbstractBlock:
        return MeltingIceBlock()
