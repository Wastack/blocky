import tkinter
from tkinter.font import Font
from typing import Callable

from gui.utils import BLOCK_SIZE


class CounterButton:
    __COLOR_RELEASED = "#D4F5A8"
    __COLOR_PUSHED = "#C3E497"
    __COLOR_MOUSEOVER = "#EEFFBB"

    def __init__(self, canvas: tkinter.Canvas,  pos: (int, int), size: int,
                 initial_value=0):
        self._canvas = canvas
        self._pos = pos
        self._size = size
        self._gids = []
        self._counter = initial_value
        self._bg_rect = None
        self._callback = None

    @property
    def value(self):
        return self._counter

    def set_change_callback(self, callback: Callable[[int],None]):
        self._callback = callback

    def draw(self):
        self.destroy()
        self._bg_rect = self._canvas.create_rectangle(
            self._pos[0], self._pos[1],
            self._pos[0] + self._size,
            self._pos[1] + self._size,
            fill=CounterButton.__COLOR_RELEASED,
            activefill=CounterButton.__COLOR_MOUSEOVER,
        )
        self._gids.append(self._bg_rect)
        times = Font(family="Times", size=str(BLOCK_SIZE), weight="bold")
        self._gids.append(
            self._canvas.create_text(self._pos[0] + self._size // 2,
                                     self._pos[1] + self._size // 2,
                                     text=str(self._counter),
                                     fill="DeepSkyBlue1", font=times))

        for gid in self._gids:
            self._canvas.tag_bind(gid, "<ButtonRelease>",
                                  self._released)
            self._canvas.tag_bind(gid, "<ButtonPress-1>",
                                  self._left_clicked)
            self._canvas.tag_bind(gid, "<ButtonPress-2>",
                                  self._right_clicked)

    def destroy(self):
        for gid in self._gids:
            self._canvas.unbind_all(gid)
            self._canvas.delete(gid)
        self._gids.clear()

    def _left_clicked(self, _event):
        self._clicked()
        self._counter += 1
        if self._callback is not None:
            self._callback(self._counter)
        self.draw()

    def _right_clicked(self, _event):
        self._clicked()
        if self._counter > -1:
            self._counter -= 1
            if self._callback is not None:
                self._callback(self._counter)
        self.draw()

    def _clicked(self):
        self._canvas.itemconfig(self._bg_rect, activefill=CounterButton.__COLOR_PUSHED)

    def _released(self, event):
        self._canvas.itemconfig(self._bg_rect,
                                activefill=CounterButton.__COLOR_MOUSEOVER)
