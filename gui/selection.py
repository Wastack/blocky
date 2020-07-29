import logging
from dataclasses import dataclass
from tkinter import Canvas
from typing import List, Iterable

from game.utils.position import Position
from gui.utils import rect_from_pos

@dataclass
class _Element:
    view : int
    pos: Position


class Selector:
    def __init__(self, canvas: Canvas):
        self._selections: List[_Element] = []
        self._canvas = canvas

    @property
    def has_selection(self) -> bool:
        return self._selections != []

    def deselect(self):
        for sel in self._selections:
            self._canvas.delete(sel.view)
        self._selections = []

    def select(self, pos:Position):
        rect_pos = rect_from_pos(pos)
        rect = self._canvas.create_rectangle(*rect_pos, width=5, outline="yellow")
        self._selections.append(_Element(view=rect, pos=pos))

    def positions(self) -> Iterable[Position]:
        return (e.pos for e in self._selections)