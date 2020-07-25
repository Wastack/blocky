from tkinter import Canvas
from typing import Optional, List

from game.utils.position import Position
from gui.block_views.block import BLOCK_SIZE, BlockView
from gui.utils import rect_from_pos


class Selector:
    def __init__(self, canvas: Canvas):
        self._selections: List[int] = []
        self._canvas = canvas

    @property
    def has_selection(self) -> bool:
        return self._selections != []

    def deselect(self):
        for sel in self._selections:
            self._canvas.delete(sel)
        self._selections = []

    def select(self, pos:Position):
        rect_pos = rect_from_pos(pos)
        rect = self._canvas.create_rectangle(*rect_pos, width=5, outline="yellow")
        self._selections.append(rect)

class MouseController:
    def __init__(self, canvas, map):
        self._canvas = canvas
        self._selection = Selector(canvas)

    def register_canvas_events(self):
        self._canvas.bind("<Button-1>", self._clicked)
        self._canvas.bind("<Shift-Button-1>", self._shift_clicked)

    @staticmethod
    def _mouse_pos_to_game_pos(x, y) -> Position:
        return Position(x // BLOCK_SIZE, y // BLOCK_SIZE)

    def _shift_clicked(self, mouse_event):
        pos = MouseController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._selection.select(pos)

    def _clicked(self, mouse_event):
        self._selection.deselect()
        self._shift_clicked(mouse_event)
