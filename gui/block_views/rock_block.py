import tkinter
from typing import Optional, Any, List

from game.blocks.block import AbstractBlock
from game.blocks.impl.rock import RockBlock
from game.blocks.walls.killer_wall import KillerWall
from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block import BlockView
from gui.block_views.block_capability import BlockCapability
from gui.block_views.wall_views import wall_factory
from gui.block_views.wall_views.wall_view import WallView


class RockBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas)
        self._wall_views: List[WallView] = []
        self._png_file_name = "brick.png"

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != RockBlock:
            return None

        rock_view = RockBlockView(canvas)
        rock_view._block = block
        return rock_view

    def draw(self, pos: Position) -> Any:
        self.destroy()

        # Draw rectangle with rock identifier
        rect = super().draw(pos)

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

    @staticmethod
    def repr() -> str:
        return "Stone"

    @staticmethod
    def block_capability() -> BlockCapability:
        return BlockCapability(possible_wall_types=frozenset([KillerWall]))

    def set_wall(self, side: Direction, wall: Optional[Wall]):
        self._block.walls().set_side(wall, side)

    def _set_default_block(self) -> AbstractBlock:
        return RockBlock()

