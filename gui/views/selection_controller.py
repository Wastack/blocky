import logging
from tkinter import Canvas, CURRENT
from typing import Type, Optional

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

        self._head: Optional[Position] = None

    def register_canvas_events(self):
        self._canvas.bind("<Button-1>", self._clicked)
        self._canvas.bind("<Control-Button-1>", self._control_clicked)
        self._canvas.bind("<Shift-Button-1>", self._shift_clicked)

    def set_exception(self, mouse_range: MouseRange, key: str, enable_shift_select=False):
        self._exceptions[key] = (mouse_range, enable_shift_select)

    def _in_exception(self, x, y, shift_candidate: bool = False) -> bool:
        """Check if mouse position is in exception"""
        if shift_candidate:
            ranges = [v for v, shift_enabled in self._exceptions.values() if not shift_enabled]
        else:
            ranges = [v for v, _ in self._exceptions.values()]
        return any([e.contains(x, y) for e in ranges])

    def _game_pos_in_exception(self, p: Position, shift_candidate: bool = False):
        """Check if a block intersects with an exception"""
        left_most = p.x * BLOCK_SIZE, p.y*BLOCK_SIZE
        bottom_right = left_most[0]+BLOCK_SIZE, left_most[1]+BLOCK_SIZE
        return self._in_exception(*left_most, shift_candidate=shift_candidate) \
            or self._in_exception(*bottom_right, shift_candidate=shift_candidate)

    def _select(self, pos):
        self._head = pos
        self._selector.select(pos)

    @staticmethod
    def _mouse_pos_to_game_pos(x, y) -> Position:
        return Position(x // BLOCK_SIZE, y // BLOCK_SIZE)

    def _shift_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return

        # If no selections were made yet, shift click works pretty much like simple click
        if self._head is None:
            self._clicked(mouse_event)
            return

        pos = SelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        for x in range(min(pos.x, self._head.x), max(pos.x, self._head.x) + 1):
            for y in range(min(pos.y, self._head.y), max(pos.y, self._head.y) + 1):
                p = Position(x, y)
                if self._game_pos_in_exception(p, shift_candidate=True):
                    continue
                self._selector.select(p)
        self._head = pos

    def _control_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        pos = SelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._select(pos)

    def _clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        self._selector.deselect()
        self._control_clicked(mouse_event)
    
    def put_block_to_selection(self, block_type: Type[BlockView]):
        if not self._selector.has_selection:
            return
        for p in self._selector.positions():
            logging.debug("Replace with {} at {}".format(block_type, p))
            self._map.replaceAt(p, block_type(self._canvas))
