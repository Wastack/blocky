import logging
from typing import Dict, List

from game.blocks.block import AbstractBlock
from game.gamemap import GameMap
from game.utils.MoveReports import MoveReport, MovableMoveReport
from game.utils.position import Position
from game.utils.size import Size
from gui.block_views import block_view_factory
from gui.block_views.block import BlockView


class MapView:
    def __init__(self, game_map: GameMap, canvas):
        self._canvas = canvas
        self._block_views: Dict[Position, BlockView] = {}
        self._game_map = game_map

    def draw(self):
        self.destroy()

        for x in range(self._game_map.size.width):
            for y in range(self._game_map.size.height):
                top_of_cell = self._game_map.block(Position(x, y)).top()
                bv = block_view_factory.from_block( top_of_cell, self._canvas)
                self._block_views[Position(x, y)] = bv
                bv.draw(Position(x, y))

    def cell(self, p: Position) -> AbstractBlock:
        return self._game_map.block(p).top()

    def move_view(self, p_from: Position, p_to: Position):
        bv = self._block_views.get(p_from)
        if bv is None:
            raise RuntimeError("Position is out of bounds")
        bv.move(p_from, p_to)


    def _clear_at(self, pos: Position) -> None:
        self._game_map.clearBlock(pos)

    def destroy(self):
        for bv in self._block_views.values():
            bv.destroy()
        self._block_views.clear()

    def replace_at(self, pos: Position, block: AbstractBlock):
        self._clear_at(pos)
        self._game_map.putBlock(pos, block)

    @property
    def size(self) -> Size:
        return self._game_map.size

    def resize(self, size: Size) -> bool:
        success = self._game_map.resize(size)
        if success:
            logging.debug("Resized")
            self.draw()
        return success

    @property
    def game_map(self) -> GameMap:
        return self._game_map

    def animate_reports(self, reports: List[MoveReport]):
        tmp_bvs = {}
        for r in reports:
            if isinstance(r, MovableMoveReport):
                bv = self._block_views.pop(r.position)
                if r.captured:
                    bv.destroy()
                else:
                    if r.target is None:
                        raise RuntimeError("Cannot interpret move report")
                    bv.move(r.position, r.target)
                    tmp_bvs[r.target] = bv

        # Put back moved block views
        for p, bv in tmp_bvs.items():
            self._block_views[p] = bv
