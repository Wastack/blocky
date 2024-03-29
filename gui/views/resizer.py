import logging
from tkinter import Canvas
from tkinter.font import Font
from typing import Iterable, Callable

from game.utils.position import Position
from game.utils.size import Size
from gui.utils import BLOCK_SIZE, MouseRange
from gui.views.map_view import MapView

RESIZING_RECT_SIZE = 10

RESIZING_LABEL_OFFSET = (10, -40)
RESIZING_LABEL_SIZE = (80, 40)
RESIZING_LABEL_TAG = "resizing-label-tag"


class Resizer:
    def __init__(self, canvas: Canvas, map_view: MapView, selection_controller, callback: Callable[[Size], bool]):
        self._canvas = canvas
        self._map_view = map_view
        self._selection_controller = selection_controller
        self._callback = callback

        self._resizing_rect_id: int = 0
        """The Id of the Resizing Rectangle which is at the bottom right corner of the currently available map.
           Resizing can be triggered via clicking on the Resizing Rectangle"""

        self._moving_resizing_rect_id: int = 0
        """The Id of the proposed new Resizing Rectangle during resizing event."""

        self._current_pos = Position(self._map_view.size.width, self._map_view.size.height)
        """Holds the current position (in logical unit) during resizing event"""

        self._border_id: int = 0
        """Holds the Id of the currently displayed resizing border. The border visualise the proposed map size."""

        self._size_label_id: int = 0
        """The Id of a label which represents the proposed map size with numbers."""


    @property
    def resizing_rect_id(self):
        return self._resizing_rect_id

    def _create_border(self) -> None:
        self._border_id = self._canvas.create_rectangle(0, 0, self._current_pos.x*BLOCK_SIZE, self._current_pos.y*BLOCK_SIZE,
                                                        width=3, outline="red")

    def _create_moving_label(self) -> None:
        self._size_label_id = RESIZING_LABEL_TAG
        real_x = BLOCK_SIZE*self._current_pos.x + RESIZING_LABEL_OFFSET[0]
        real_y = BLOCK_SIZE*self._current_pos.y + RESIZING_LABEL_OFFSET[1]
        vertices = [real_x,
                    real_y,
                    real_x + RESIZING_LABEL_SIZE[0],
                    real_y + RESIZING_LABEL_SIZE[1]]
        self._canvas.create_rectangle(*vertices, tag=RESIZING_LABEL_TAG, fill="wheat1")

        text = "{}x{}".format(self._current_pos.x, self._current_pos.y)
        times = Font(family="Times", size=str(RESIZING_LABEL_SIZE[1] // 2), weight="bold")
        self._canvas.create_text(real_x + RESIZING_LABEL_SIZE[0] // 2, real_y + RESIZING_LABEL_SIZE[1] // 2,
                                 text=text, fill="DeepSkyBlue4", font=times, tag=RESIZING_LABEL_TAG)

    def _create_resizing_rect(self, pos: Position) -> int:
        vs = self._resizing_rect_vertices(pos)
        return self._canvas.create_rectangle(*vs, fill="gray")

    def _resizing_rect_vertices(self, pos: Position) -> Iterable[int]:
        real_pox_x, real_pos_y = (BLOCK_SIZE*pos.x, BLOCK_SIZE*pos.y)
        rect_size_half = RESIZING_RECT_SIZE // 2
        return (real_pox_x - rect_size_half,
                real_pos_y - rect_size_half,
                real_pox_x + rect_size_half,
                real_pos_y + rect_size_half)

    def _register_mouse_events(self):
        for event_id, func in [("<Button-1>", self.start_resize),
                               ("<B1-Motion>", self.mouse_moved),
                               ("<ButtonRelease-1>", self.stop_resize)]:
            self._canvas.tag_bind(self._resizing_rect_id, event_id, func)

    def draw_resizing_rect(self):
        rect = self._create_resizing_rect(self._current_pos)
        self._resizing_rect_id = rect
        self._register_mouse_events()
        self._selection_controller.set_exception(key="resizer",
                                                 mouse_range=MouseRange(*self._resizing_rect_vertices(self._current_pos)),
                                                 enable_shift_select=True)

    def start_resize(self, mouse_e):
        self._create_border()
        self._create_moving_label()

    def stop_resize(self, _mouse_e):
        for e in filter(lambda x: x != 0, [self._moving_resizing_rect_id, self._border_id, self._size_label_id]):
            self._canvas.delete(e)
        self._moving_resizing_rect_id = 0
        self._border_id = 0
        self._size_label_id = 0

        if not self._callback:
            logging.warning("No callback is registered to Resizer object.")
            return

        succeed = self._callback(Size(width=self._current_pos.x, height=self._current_pos.y))
        if succeed:
            self._canvas.delete(self._resizing_rect_id)
            self.draw_resizing_rect()

    def mouse_moved(self, mouse_e):
        new_pos = Position(int(mouse_e.x / BLOCK_SIZE + 0.5), int(mouse_e.y / BLOCK_SIZE + 0.5))
        if new_pos == self._current_pos:
            return
        self._current_pos = new_pos

        # Move border
        self._canvas.delete(self._border_id)
        self._create_border()

        # Move resizing rect
        if self._moving_resizing_rect_id != 0:
            self._canvas.delete(self._moving_resizing_rect_id)
        self._moving_resizing_rect_id = self._create_resizing_rect(new_pos)

        # Move resizing label
        if self._size_label_id != 0:
            self._canvas.delete(self._size_label_id)
        self._create_moving_label()

    def refresh(self):
        if self._resizing_rect_id:
            self._canvas.delete(self._resizing_rect_id)
        self._current_pos = Position(self._map_view.size.width, self._map_view.size.height)
        self.draw_resizing_rect()

    def destroy(self):
        if self._resizing_rect_id:
            self._canvas.delete(self._resizing_rect_id)
            self._resizing_rect_id = None
