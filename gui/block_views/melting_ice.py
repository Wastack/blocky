import tkinter
from typing import Optional, Any, Dict

from game.blocks.block import AbstractBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block import BlockView
from gui.block_views.block_capability import BlockCapability
from gui.block_views.wall_views import wall_factory
from gui.block_views.wall_views.empty_wall_view import EmptyWallView
from gui.block_views.wall_views.spike import SpikeView
from gui.block_views.wall_views.wall_view import WallView


class MeltingIceBlockView(BlockView):
    def __init__(self, canvas: tkinter.Canvas, life=1):
        super().__init__(canvas, block_fill_color="purple")
        self._text_id = None
        self._wall_views: Dict[Direction, Optional[WallView]] = {
            Direction.UP: None,
            Direction.LEFT: None,
            Direction.DOWN: None,
            Direction.RIGHT: None,
        }
        self._life = life

    @staticmethod
    def from_block(canvas: tkinter.Canvas, block: MeltingIceBlock) -> Optional['BlockView']:
        if type(block) != MeltingIceBlock:
            return None

        rock_view = MeltingIceBlockView(canvas, life=block.life)
        if block.walls():
            for side, wall in block.walls().walls().items():
                if not wall:
                    continue
                rock_view.set_wall(side,
                                   wall_factory.from_wall(wall, side, canvas))
        return rock_view

    def draw(self, pos: Position) -> Any:
        if self._text_id is not None:
            self.destroy()

        # Draw rectangle with Melting identifier
        rect = super().draw(pos)
        self._text_id = self._create_text(pos, text=f"{self._life}")

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
        return "MeltingIce"

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

    def to_game_block(self) -> AbstractBlock:
        return MeltingIceBlock(WallView.to_wall_container(self._wall_views))
