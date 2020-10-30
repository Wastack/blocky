import logging
from abc import ABC, abstractmethod
from tkinter import Canvas
from typing import List, Any, Iterable


class SelectionController(ABC):
    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._selected_items: List[(int, Any)] = []

    def register_canvas_events(self, click: bool, shift: bool = False, control: bool = False):
        if click:
            self._canvas.bind("<Button-1>", self._clicked)
        if shift:
            self._canvas.bind("<Shift-Button-1>", self._shift_clicked)
        if control:
            self._canvas.bind("<Control-Button-1>", self._control_clicked)

    def _set_selection(self, mouse_pos: (int, int), size: int, item: Any):
        rect = self._canvas.create_rectangle(*mouse_pos,
                                             *[m + size for m in mouse_pos],
                                             width=5, outline="yellow")
        self._selected_items.append((rect, item))

    @property
    def selected_items(self) -> Iterable[Any]:
        return (i for _, i in self._selected_items)

    def deselect_all(self):
        for gid, _ in self._selected_items:
            self._canvas.delete(gid)
        self._selected_items = []

    def has_selection(self) -> bool:
        return self._selected_items != []

    @abstractmethod
    def _clicked(self, mouse_event):
        raise NotImplementedError

    @abstractmethod
    def _control_clicked(self, mouse_event):
        raise NotImplementedError

    @abstractmethod
    def _shift_clicked(self, mouse_event):
        raise NotImplementedError
