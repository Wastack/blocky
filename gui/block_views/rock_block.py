import logging
import tkinter
from typing import Optional, Any, Dict

from game.blocks.impl.rock import RockBlock
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block import BlockView
from gui.block_views.block_capability import BlockCapability
from gui.block_views.wall_views import wall_factory
from gui.block_views.wall_views.empty_wall_view import EmptyWallView
from gui.block_views.wall_views.spike import SpikeView
from gui.block_views.wall_views.wall_view import WallView


class RockBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas):
        super().__init__(canvas)
        self._text_id = None
        self._wall_views: Dict[Direction, Optional[WallView]] = {
            Direction.UP: None,
            Direction.LEFT: None,
            Direction.DOWN: None,
            Direction.RIGHT: None,
        }

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        if type(block) != RockBlock:
            return None

        rock_view = RockBlockView(canvas)
        if block.walls():
            for side, wall in block.walls().walls().items():
                if not wall:
                    continue
                rock_view.set_wall(side, wall_factory.from_wall(wall, side, canvas))
        return rock_view

    def draw(self, pos: Position) -> Any:
        if self._text_id is not None:
            self.destroy()

        # Draw rectangle with rock identifier
        rect = super().draw(pos)
        self._text_id = self._create_text(pos, text="R")

        # Draw walls
        for side, wall_view in self._wall_views.items():
            if wall_view is None:
                continue
            wall_view.draw(pos)
            pass
            
        return rect

    def destroy(self):
        super().destroy()
        for w in self._wall_views.values():
            if w is None:
                continue
            w.destroy()
        if self._text_id is not None:
            self._canvas.delete(self._text_id)
            self._text_id = None

    @staticmethod
    def repr() -> str:
        return "Stone"

    @staticmethod
    def block_capability() -> BlockCapability:
        return BlockCapability(possible_wall_types=frozenset([SpikeView]))

    def set_wall(self, side: Direction, wall_view: WallView):
        previous = self._wall_views.get(side)
        if previous:
            previous.destroy()
            self._wall_views[side] = None
        if isinstance(wall_view, EmptyWallView):
            return
        self._wall_views[side] = wall_view
