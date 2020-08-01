import logging
from tkinter import Canvas, CURRENT
from typing import Type

from game.utils.position import Position
from gui.block_views.block import BLOCK_SIZE, BlockView
from gui.selection import Selector
from gui.utils import MouseRange
from gui.views.map_view import MapView


class SelectionController:
    def __init__(self, canvas: Canvas, map: MapView):
        self._map = map
        self._canvas = canvas
        self._selector = Selector(canvas)
        self._exceptions = {}

    def register_canvas_events(self):
        self._canvas.bind("<Button-1>", self._clicked)
        self._canvas.bind("<Shift-Button-1>", self._shift_clicked)

    def set_exception(self, range: MouseRange, key: str):
        self._exceptions[key] = range

    def _in_exception(self, x, y) -> bool:
        return any([e.contains(x, y) for e in self._exceptions.values()])


    @staticmethod
    def _mouse_pos_to_game_pos(x, y) -> Position:
        return Position(x // BLOCK_SIZE, y // BLOCK_SIZE)

    def _shift_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        pos = SelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._selector.select(pos)

    def _clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        self._selector.deselect()
        self._shift_clicked(mouse_event)
    
    def put_block_to_selection(self, block_type: Type[BlockView]):
        if not self._selector.has_selection:
            return
        for p in self._selector.positions():
            logging.debug("Replace with {} at {}".format(block_type, p))
            self._map.replaceAt(p, block_type(self._canvas))
