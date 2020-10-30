import logging
from sys import platform as _platform

from dataclasses import dataclass
from tkinter import Canvas
from tkinter.font import Font
from typing import List, Callable, Type

from gui.block_views.block import BlockView
from gui.block_views.block_view_factory import registered_block_views

PALETTE_WIDTH = 80
ONE_BLOCK_HEIGHT = 25
HEIGHT_MARGIN = 15

NOT_SELECTED_FILL = "AntiqueWhite1"
SELECTED_FILL = "Yellow"
TEXT_FILL = "DeepSkyBlue4"


@dataclass
class _BlockElement:
    text: int
    rectangle: int


class Palette:
    """
    Palette is a pop-up menu used for selecting a block type to insert.
    """

    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._callback = None

        self._block_elements: List[_BlockElement] = []

        self._mouse_pressed_x = 0
        self._mouse_pressed_y = 0

        self._selected_block_index = 0

    def _show(self, mouse_event):
        self._mouse_pressed_x, self._mouse_pressed_y = mouse_event.x, mouse_event.y
        self._create_palette(mouse_event.x, mouse_event.y)

    def _index_from_mouse_y_pos(self, y):
        return (y - self._mouse_pressed_y) // ONE_BLOCK_HEIGHT

    def _catch_and_destroy(self, mouse_event):
        index = self._index_from_mouse_y_pos(mouse_event.y)

        # clear palette
        for elem in self._block_elements:
            self._canvas.delete(elem.text)
            self._canvas.delete(elem.rectangle)
        self._block_elements = []

        # publish result
        if 0 <= index < len(registered_block_views):
            block_view = registered_block_views[index]
            self._callback(block_view)

    def _motion(self, mouse_event):
        index = self._index_from_mouse_y_pos(mouse_event.y)
        if self._selected_block_index == index:
            return
        if not (0 <= index < len(self._block_elements)):
            return
        self._canvas.itemconfig(self._block_elements[self._selected_block_index].rectangle, fill=NOT_SELECTED_FILL)
        self._canvas.itemconfig(self._block_elements[index].rectangle, fill=SELECTED_FILL)
        self._selected_block_index = index

    def _create_rect(self, x, y, height, fill):
        background = self._canvas.create_rectangle(x, y,
                                                   x + PALETTE_WIDTH, y + height, fill=fill)
        return background

    def _create_palette(self, mouse_x: int, mouse_y: int) -> None:
        text_pos_x = mouse_x + PALETTE_WIDTH // 2
        text_pos_y = mouse_y + HEIGHT_MARGIN
        text_font = Font(family="Times", size=str(10), weight="bold")
        for cls in registered_block_views:
            rect = self._canvas.create_rectangle(mouse_x, text_pos_y-15, mouse_x + PALETTE_WIDTH, text_pos_y + 10, fill=NOT_SELECTED_FILL)
            text = self._canvas.create_text(text_pos_x, text_pos_y, text=cls.repr(), fill=TEXT_FILL, font=text_font)
            self._block_elements.append(_BlockElement(text, rect))
            text_pos_y += ONE_BLOCK_HEIGHT
        self._canvas.itemconfig(self._block_elements[0].rectangle, fill=SELECTED_FILL)

    def register_right_mouse(self, callback: Callable[[Type[BlockView]], None]) -> None:
        """
        Registers right mouse events.
        """
        logging.info("Palette registered to right click mouse button.")
        self._callback = callback

        # On Mac right mouse button is signed by 2 instead of 3
        right_mouse_id = "2" if _platform == "darwin" else "3"

        self._canvas.bind(f"<Button-{right_mouse_id}>", self._show)
        self._canvas.bind("<Motion>", self._motion)
        self._canvas.bind(f"<ButtonRelease-{right_mouse_id}>", self._catch_and_destroy)
