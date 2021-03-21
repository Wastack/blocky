from game.blocks.block import AbstractBlock
from game.gamemap import GameMap
from game.utils.position import Position
from game.utils.size import Size
from gui.block_views import block_view_factory


class MapView:
    def __init__(self, game_map: GameMap, canvas):
        self._canvas = canvas
        self._block_views = []
        self._game_map = game_map

    def draw(self):
        self.destroy()

        for x in range(self._game_map.size.width):
            for y in range(self._game_map.size.height):
                top_of_cell = self._game_map.block(Position(x, y)).top()
                bv = block_view_factory.from_block( top_of_cell, self._canvas)
                self._block_views.append(bv)
                bv.draw(Position(x, y))

    def cell(self, p: Position) -> AbstractBlock:
        return self._game_map.block(p).top()

    def _clear_at(self, pos: Position) -> None:
        self._game_map.clearBlock(pos)

    def destroy(self):
        for bv in self._block_views:
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
            self.draw()
        return success

    @property
    def game_map(self) -> GameMap:
        return self._game_map
