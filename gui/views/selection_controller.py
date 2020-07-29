import logging
from typing import Type

from game.utils.position import Position
from gui.block_views.block import BLOCK_SIZE, BlockView
from gui.selection import Selector
from gui.views.map_view import MapView


class SelectionController:
    def __init__(self, canvas, map: MapView):
        self._map = map
        self._canvas = canvas
        self._selector = Selector(canvas)

    def register_canvas_events(self):
        self._canvas.bind("<Button-1>", self._clicked)
        self._canvas.bind("<Shift-Button-1>", self._shift_clicked)

    @staticmethod
    def _mouse_pos_to_game_pos(x, y) -> Position:
        return Position(x // BLOCK_SIZE, y // BLOCK_SIZE)

    def _shift_clicked(self, mouse_event):
        pos = SelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._selector.select(pos)

    def _clicked(self, mouse_event):
        self._selector.deselect()
        self._shift_clicked(mouse_event)
    
    def put_block_to_selection(self, block_type: Type[BlockView]):
        if not self._selector.has_selection:
            return
        for p in self._selector.positions():
            logging.debug("Replace with {} at {}".format(block_type, p))
            self._map.replaceAt(p, block_type(self._canvas))
