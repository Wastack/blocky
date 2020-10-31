import logging
from dataclasses import dataclass
from tkinter import Canvas
from tkinter.font import Font
from typing import Optional

from game.utils.direction import Direction
from gui.utils import WINDOW_WIDTH, BLOCK_SIZE, MouseRange, \
    tkinter_right_mouse_button, ButtonEventType
from gui.controllers.block_selection_controller import BlockSelectionController

PROPERTY_SETTINGS_WINDOW_WIDTH = WINDOW_WIDTH // 5
PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN = 5

WALL_SETTINGS_VERTICAL_OFFSET = 35
WALL_SETTINGS_MARGIN = 10
WALL_SETTINGS_HEIGHT = 160


@dataclass
class _WallSelection:
    gid: Optional[int] = None
    is_selected: bool = False


class PropertySettings:

    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._drawn_ids = []

        # Register to resize event
        self._canvas.bind("<Configure>", self._on_resize)

        self._leftmost_pos = 0
        self._rightmost_pos = 0

        self._wall_selectors = {
            Direction.LEFT: _WallSelection(),
            Direction.DOWN: _WallSelection(),
            Direction.RIGHT: _WallSelection(),
            Direction.UP: _WallSelection()
        }

    def draw_settings_window(self):
        # canvas update is needed to query canvas size
        self._canvas.update()

        sw, sh = self._canvas.winfo_width(), self._canvas.winfo_height()
        self._leftmost_pos = sw - PROPERTY_SETTINGS_WINDOW_WIDTH
        self._rightmost_pos = sw
        logging.debug(f"Resizing settings window X: {self._leftmost_pos} to {self._rightmost_pos}")

        # Draw border of settings window
        self._drawn_ids.append(
            self._canvas.create_rectangle(self._leftmost_pos, 0,
                                          sw, sh, fill="gray5"))

        # Draw text for wall properties part
        times = Font(family="Times", size=str(BLOCK_SIZE // 2), weight="bold")
        self._drawn_ids.append(
            self._canvas.create_text(self._leftmost_pos + 40, 20, text="Walls:",
                                     fill="DeepSkyBlue1", font=times)
        )

        # Draw bounding box for wall properties
        self._draw_bounding_box(y=WALL_SETTINGS_VERTICAL_OFFSET, height=WALL_SETTINGS_HEIGHT)

        # Draw wall side selector which consists of 4 rectangles
        offsets = [
            (Direction.UP, [1, 0, 3, 1]),
            (Direction.LEFT, [0, 1, 1, 3]),
            (Direction.DOWN, [1, 3, 3, 4]),
            (Direction.RIGHT, [3, 1, 4, 3]),
        ]
        multiplier = WALL_SETTINGS_HEIGHT // 4
        x_padding = (self._rightmost_pos - self._leftmost_pos - 2 * PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN - WALL_SETTINGS_HEIGHT) // 2
        for side, rect_offset in offsets:
            mo = [r * multiplier for r in rect_offset]
            rect = self._canvas.create_rectangle(mo[0] + self._leftmost_pos + PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN + x_padding,
                                                 mo[1] + WALL_SETTINGS_VERTICAL_OFFSET,
                                                 mo[2] + self._leftmost_pos + PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN + x_padding,
                                                 mo[3] + WALL_SETTINGS_VERTICAL_OFFSET,
                                                 fill="#D4F5A8")

            wall_selector = self._wall_selectors[side]
            wall_selector.gid = rect
            self._canvas.tag_bind(rect, "<Button-1>", self._toggle_select)
            self._canvas.tag_bind(rect, tkinter_right_mouse_button(ButtonEventType.CLICK), self._open_wall_palette)
            self._canvas.tag_bind(rect, tkinter_right_mouse_button(ButtonEventType.RELEASE), self._execute_and_hide_wall_palette)

    def _toggle_select(self, mouse_event):
        raise NotImplementedError()

    def _open_wall_palette(self, mouse_event):
        raise NotImplementedError()

    def _execute_and_hide_wall_palette(self, mouse_event):
        raise NotImplementedError()

    def _on_resize(self, _event):
        self._delete_graphical_objects()
        self.draw_settings_window()

    def _delete_graphical_objects(self):
        for i in self._drawn_ids:
            self._canvas.delete(i)
        self._drawn_ids = []
        for wall_selector in self._wall_selectors.values():
            if wall_selector.gid is not None:
                self._canvas.delete(wall_selector.gid)
                wall_selector.gid = None

    def _draw_bounding_box(self, y: int, height: int):
        """
        Draws a bounding box from y coordinate with a height. Width of the
        bounding box depends on margin.
        """
        self._drawn_ids.append(
            self._canvas.create_rectangle(self._leftmost_pos + PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN, y,
                                          self._rightmost_pos - PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN, y + height,
                                          fill="#F5F5A8")
        )
