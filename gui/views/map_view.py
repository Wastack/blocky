import logging

from game.gamemap import GameMap
from game.utils.position import Position
from game.utils.size import Size
from gui.block_views import block_view_factory
from gui.block_views.block import BlockView
from gui.block_views.empty_block import EmptyBlockView


class MapView:
    def __init__(self, game_map:GameMap, canvas):
        self._canvas = canvas
        self._block_views = []
        for column in game_map._blocks[:]:
            view_column = []
            self._block_views.append(view_column)
            for stack in column:
                view_stack = []
                view_column.append(view_stack)
                blocks = stack.data()
                if not blocks:
                    view_stack.append(EmptyBlockView(canvas))
                else:
                    for block in stack.data():
                        view_stack.append(block_view_factory.from_block(block, canvas))

    def draw(self):
        for x, col in enumerate(self._block_views):
            for y, cell in enumerate(col):
                for b in cell:
                    b.draw(Position(x, y))

    def _clear_at(self, pos: Position) -> None:
        stack = self._block_views[pos.x][pos.y]
        for e in stack:
            e.destroy()
        stack.clear()

    def replaceAt(self, pos: Position, block: BlockView):
        self._clear_at(pos)
        stack = self._block_views[pos.x][pos.y]
        stack.append(block)
        block.draw(pos)

    @property
    def size(self) -> Size:
        if not self._block_views:
            return Size(0, 0)
        return Size(width=len(self._block_views), height=len(self._block_views[0]))

    def resize(self, size: Size) -> bool:
        current = self.size
        d_width, d_height = size.width - current.width, size.height - current.height
        logging.debug("Diff: width: {}, height: {}".format(d_width, d_height))

        # Height
        if d_height < 0:
            for i, col in enumerate(self._block_views):
                for cell in col[len(col) + d_height:]:
                    for b in cell:
                        b.destroy()
                self._block_views[i] = col[:len(col) + d_height]
        else:
            for col in self._block_views:
                for _ in range(d_height):
                    col.append([EmptyBlockView(self._canvas)])

        # Width
        if d_width < 0:
            for col in self._block_views[len(self._block_views) + d_width:]:
                for cell in col:
                    for b in cell:
                        b.destroy()
            self._block_views = self._block_views[:len(self._block_views) + d_width]
        else:
            for _ in range(d_width):
                col = []
                self._block_views.append(col)
                for _ in range(size.height):
                    col.append([EmptyBlockView(self._canvas)])
            self.draw()
        return True
