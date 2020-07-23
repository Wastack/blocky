import tkinter
from typing import Any

from game.utils.position import Position

_BLOCK_SIZE = 20


class BlockView():
    def __init__(self, canvas: tkinter.Canvas, pos: Position):
        self._pos = pos
        self._canvas = canvas

    def _on_left_mouse(self, event):
        print("Mouse event received: {}".format(event))

    def draw(self) -> 'BlockView':
        rect = self._create_block()
        self._canvas.tag_bind(rect, "<1>", self._on_left_mouse)
        return self


    def _create_block(self) -> Any:
        rect = [self._pos.x*_BLOCK_SIZE, self._pos.y*_BLOCK_SIZE,
                self._pos.x*_BLOCK_SIZE + _BLOCK_SIZE, self._pos.y*_BLOCK_SIZE,
                self._pos.x * _BLOCK_SIZE + _BLOCK_SIZE, self._pos.y * _BLOCK_SIZE + _BLOCK_SIZE,
                self._pos.x * _BLOCK_SIZE , self._pos.y * _BLOCK_SIZE + _BLOCK_SIZE,
                ]
        return self._canvas.create_polygon(*rect, fill="red")
