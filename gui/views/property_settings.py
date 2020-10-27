from tkinter import Canvas
from tkinter.font import Font

from gui.utils import WINDOW_WIDTH, BLOCK_SIZE, MouseRange
from gui.views.selection_controller import SelectionController

PROPERTY_SETTINGS_WINDOW_WIDTH = WINDOW_WIDTH // 5


class PropertySettings:
    def __init__(self, canvas: Canvas,
                 selection_controller: SelectionController):
        self._canvas = canvas
        self._drawn_ids = []
        self._selection_controller = selection_controller

        # Register to resize event
        self._canvas.bind("<Configure>", self._on_resize)

        self._leftmost_pos = 0
        self._rightmost_pos = 0

    def draw_settings_window(self):
        # canvas update is needed to query canvas size
        self._canvas.update()

        sw, sh = self._canvas.winfo_width(), self._canvas.winfo_height()
        self._leftmost_pos = sw - PROPERTY_SETTINGS_WINDOW_WIDTH
        self._rightmost_pos = sw

        # Draw border of settings window
        self._drawn_ids.append(
            self._canvas.create_rectangle(self._leftmost_pos, 0,
                                          sw, sh // 2, fill="#F5F5A8"))

        # Add selection window as an exception for selection controller.
        # One does not simply select a rectangle under the settings window.
        leftmost_rounded = self._leftmost_pos - self._leftmost_pos % BLOCK_SIZE
        height_rounded = sh//2 - sh//2 % BLOCK_SIZE + BLOCK_SIZE
        self._selection_controller.set_exception(key="Settings_window",
                                                 mouse_range=MouseRange(
                                                     x1=leftmost_rounded,
                                                     y1=0, x2=sw, y2=height_rounded))

        # Draw text for wall properties part
        times = Font(family="Times", size=str(BLOCK_SIZE // 2), weight="bold")
        self._drawn_ids.append(
            self._canvas.create_text(self._leftmost_pos + 40, 20, text="Walls:",
                                     fill="DeepSkyBlue4", font=times)
        )
        # Draw bounding box for wall properties
        self._draw_bounding_box(35, 150)

    def _on_resize(self, _event):
        for i in self._drawn_ids:
            self._canvas.delete(i)
        self._drawn_ids = []
        self.draw_settings_window()

    def _draw_bounding_box(self, y: int, height: int):
        """
        Draws a bounding box from y coordinate with a height. Width of the
        bounding box depends on margin.
        """
        self._drawn_ids.append(
            self._canvas.create_rectangle(self._leftmost_pos + 5, y,
                                          self._rightmost_pos - 5, y + height,
                                          fill=None)
        )
