import functools
import logging

from dataclasses import dataclass
from tkinter import Canvas
from tkinter.font import Font
from typing import List, Callable, Type, Any

from gui.utils import tkinter_right_mouse_button, ButtonEventType

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

    def __init__(self, canvas: Canvas, available_items: List[Any]):
        self._canvas = canvas
        self._callback = None

        self._block_elements: List[_BlockElement] = []

        self._mouse_pressed_x = 0
        self._mouse_pressed_y = 0

        self._selected_index = 0
        self._items = available_items

    def show(self, mouse_event):
        self._mouse_pressed_x, self._mouse_pressed_y = mouse_event.x, mouse_event.y
        self._create_palette(mouse_event.x, mouse_event.y)

    def _index_from_mouse_y_pos(self, y):
        return (y - self._mouse_pressed_y) // ONE_BLOCK_HEIGHT

    def catch_and_destroy(self, mouse_event):
        index = self._index_from_mouse_y_pos(mouse_event.y)

        # clear palette
        for elem in self._block_elements:
            self._canvas.delete(elem.text)
            self._canvas.delete(elem.rectangle)
        self._block_elements = []

        # publish result
        if 0 <= index < len(self._items):
            if not self._callback:
                logging.warning("Palette used without a callback")
            else:
                item = self._items[index]
                self._callback(item)

    def _motion(self, mouse_event):
        index = self._index_from_mouse_y_pos(mouse_event.y)
        if self._selected_index == index:
            return
        if not (0 <= index < len(self._block_elements)):
            return
        self._canvas.itemconfig(self._block_elements[self._selected_index].rectangle, fill=NOT_SELECTED_FILL)
        self._canvas.itemconfig(self._block_elements[index].rectangle, fill=SELECTED_FILL)
        self._selected_index = index

    def _create_rect(self, x, y, height, fill):
        background = self._canvas.create_rectangle(x, y,
                                                   x + PALETTE_WIDTH, y + height, fill=fill)
        return background

    def _create_palette(self, mouse_x: int, mouse_y: int) -> None:
        text_pos_x = mouse_x + PALETTE_WIDTH // 2
        text_pos_y = mouse_y + HEIGHT_MARGIN
        text_font = Font(family="Times", size=str(10), weight="bold")
        for item in self._items:
            rect = self._canvas.create_rectangle(mouse_x, text_pos_y-15, mouse_x + PALETTE_WIDTH, text_pos_y + 10, fill=NOT_SELECTED_FILL)
            text = self._canvas.create_text(text_pos_x, text_pos_y, text=item.repr(), fill=TEXT_FILL, font=text_font)
            self._block_elements.append(_BlockElement(text, rect))
            text_pos_y += ONE_BLOCK_HEIGHT
        self._canvas.itemconfig(self._block_elements[0].rectangle, fill=SELECTED_FILL)

    def register_right_mouse(self, callback: Callable[[Type[Any]], None], item_to_register: Any = None) -> None:
        """
        Registers right mouse events.
        :param item_to_register Item on which the events are to be registered.
            If None, the events will be registered on the canvas.
        """
        self._callback = callback

        register_on = self._canvas if item_to_register is None else item_to_register

        if isinstance(register_on, int):
            bind_fun = functools.partial(self._canvas.tag_bind, register_on)
        else:
            bind_fun = self._canvas.bind

        bind_fun(tkinter_right_mouse_button(ButtonEventType.CLICK), self.show)
        bind_fun("<Motion>", self._motion)
        bind_fun(tkinter_right_mouse_button(ButtonEventType.RELEASE), self.catch_and_destroy)
