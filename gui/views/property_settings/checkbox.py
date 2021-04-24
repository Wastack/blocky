import tkinter
from tkinter.font import Font
from typing import Callable

from gui.utils import BLOCK_SIZE


class CheckBox:
    __COLOR_OFF = "#D4F5A8"
    __COLOR_ON = "#C3E497"
    __COLOR_MOUSEOVER = "#EEFFBB"

    def __init__(self, canvas: tkinter.Canvas,  pos: (int, int), size: int,
                 is_checked=False):
        self._canvas = canvas
        self._pos = pos
        self._size = size
        self._gids = []
        self._is_checked = is_checked
        self._bg_rect = None
        self._callback = None

    @property
    def value(self) -> bool:
        return self._is_checked

    def set_change_callback(self, callback: Callable[[bool],None]):
        self._callback = callback

    def draw(self):
        self.destroy()
        self._bg_rect = self._canvas.create_rectangle(
            self._pos[0], self._pos[1],
            self._pos[0] + self._size,
            self._pos[1] + self._size,
            fill=CheckBox.__COLOR_ON if self._is_checked else CheckBox.__COLOR_OFF,
            activefill=CheckBox.__COLOR_MOUSEOVER,
            )
        self._gids.append(self._bg_rect)
        times = Font(family="Times", size=str(BLOCK_SIZE), weight="bold")
        if self._is_checked:
            self._gids.append(
                self._canvas.create_text(self._pos[0] + self._size // 2,
                                         self._pos[1] + self._size // 2,
                                         text="✓",
                                         fill="DeepSkyBlue1", font=times))

        for gid in self._gids:
            self._canvas.tag_bind(gid, "<ButtonPress-1>",
                                  self._left_clicked)

    def destroy(self):
        for gid in self._gids:
            self._canvas.unbind_all(gid)
            self._canvas.delete(gid)
        self._gids.clear()

    def _left_clicked(self, _event):
        self._is_checked = not self._is_checked
        if self._callback is not None:
            self._callback(self._is_checked)
        self.draw()

    def set_checked(self, value: bool, notify_callback: bool):
        self._is_checked = value
        if notify_callback and self._callback is not None:
            self._callback(self._is_checked)
        self.draw()
