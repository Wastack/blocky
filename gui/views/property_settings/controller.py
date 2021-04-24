import functools
from dataclasses import dataclass
from tkinter import Canvas
from tkinter.font import Font
from typing import Optional, Type

from game.blocks.impl.player import Player
from game.utils.direction import Direction
from gui.block_views.wall_views.wall_factory import registered_wall_views
from gui.block_views.wall_views.wall_view import WallView
from gui.controllers.block_selection_controller import BlockSelectionController
from gui.utils import WINDOW_WIDTH, BLOCK_SIZE
from gui.views.palette import Palette
from gui.views.property_settings.checkbox import CheckBox
from gui.views.property_settings.counter_button import CounterButton

PROPERTY_SETTINGS_WINDOW_WIDTH = WINDOW_WIDTH // 5
PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN = 5

WALL_SETTINGS_VERTICAL_OFFSET = 35
WALL_SETTINGS_MARGIN = 10
WALL_SETTINGS_HEIGHT = 160
CAPACITY_BOX_HEIGHT = 80


@dataclass
class _WallSelection:
    gid: Optional[int] = None
    is_selected: bool = False


class PropertySettings:

    def __init__(self, canvas: Canvas, block_sel_controller: BlockSelectionController):
        self._canvas = canvas
        self._block_selection_controller = block_sel_controller
        self._drawn_ids = []
        self._drawn_objects = []
        self._leftmost_pos = 0
        self._rightmost_pos = 0

        self._wall_selectors = {
            Direction.LEFT: _WallSelection(),
            Direction.DOWN: _WallSelection(),
            Direction.RIGHT: _WallSelection(),
            Direction.UP: _WallSelection()
        }

        self._palette = Palette(self._canvas, registered_wall_views)
        self._capacity_button: Optional[CounterButton] = None

        self._block_selection_controller.subscribe_changed(self._selection_controller_changed)

    def _selection_controller_changed(self):
        if self._capacity_button is None:
            return
        self._capacity_button.set_counter(0, notify_callback=False)

    def draw(self):
        # canvas update is needed to query canvas size
        self._canvas.update()

        sw, sh = self._canvas.winfo_width(), self._canvas.winfo_height()
        self._leftmost_pos = sw - PROPERTY_SETTINGS_WINDOW_WIDTH
        self._rightmost_pos = sw

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
        box = self._draw_bounding_box(y=WALL_SETTINGS_VERTICAL_OFFSET, height=WALL_SETTINGS_HEIGHT)

        # Register palette to wall settings bounding box
        self._palette.register_right_mouse(self._trigger_palette, box)

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
                                                 fill="#D4F5A8",
                                                 activefill="#EEFFBB")

            wall_selector = self._wall_selectors[side]
            if wall_selector.gid is not None:
                self._canvas.delete(wall_selector.gid)
            wall_selector.gid = rect

            # Register mouse events on wall selectors
            self._canvas.tag_bind(rect, "<Button-1>",
                                  functools.partial(self._toggle_select, wall_selector))

            # Palette has to be registered to these graphics as well,
            # because underlying rect won't capture the event.
            self._palette.register_right_mouse(self._trigger_palette, rect)

        # Draw capacity selector if applicable
        y_offset = WALL_SETTINGS_VERTICAL_OFFSET + WALL_SETTINGS_HEIGHT + 20
        self._drawn_ids.append(
            self._canvas.create_text(self._leftmost_pos + 60, y_offset, text="Capacity:",
                                     fill="DeepSkyBlue1", font=times)
        )
        y_offset = y_offset + 20
        self._draw_bounding_box(y=y_offset, height=CAPACITY_BOX_HEIGHT)
        self._capacity_button = CounterButton(self._canvas, pos=(self._leftmost_pos + 10, y_offset + 5), size=CAPACITY_BOX_HEIGHT - 2*5)

        # Inject capacity to selection controller with a callback
        self._capacity_button.set_change_callback(self._block_selection_controller.change_capacity_on_selection)

        self._capacity_button.draw()
        self._drawn_objects.append(self._capacity_button)

        # Checkbox to decide if player can move only once
        # TODO show only if at least one player is selected
        y_offset = y_offset + CAPACITY_BOX_HEIGHT + 20
        self._drawn_ids.append(
            self._canvas.create_text(self._leftmost_pos + 70, y_offset, text="Move once?",
                                     fill="DeepSkyBlue1", font=times)
        )
        y_offset = y_offset + 20
        self._draw_bounding_box(y=y_offset, height=CAPACITY_BOX_HEIGHT)
        self._player_move_checkbox = CheckBox(self._canvas, pos=(self._leftmost_pos + 10, y_offset + 5), size=CAPACITY_BOX_HEIGHT - 2*5)
        self._player_move_checkbox.set_change_callback(self._block_selection_controller.change_move_once_on_selection)
        self._player_move_checkbox.draw()
        self._drawn_objects.append(self._player_move_checkbox)


    def _trigger_palette(self, wall_view_type: Type[WallView]):
        """
        Responsible for executing placement of walls after choosing one from
        the palette.
        """
        for side, wall_sel in self._wall_selectors.items():
            if wall_sel.is_selected:
                wall_type = wall_view_type.to_game_wall()
                self._block_selection_controller.put_wall_to_selection(side, wall_type)

    def _toggle_select(self, wall_selector: _WallSelection, _mouse_event):
        wall_selector.is_selected = not wall_selector.is_selected  # toggle
        if wall_selector.is_selected:
            # draw border to indicate selected
            self._canvas.itemconfigure(wall_selector.gid, width=3)
        else:
            # undo selection indicator graphic
            self._canvas.itemconfigure(wall_selector.gid, width=1)

    def _delete_graphical_objects(self):
        for i in self._drawn_ids:
            self._canvas.delete(i)
        self._drawn_ids.clear()

        for wall_selector in self._wall_selectors.values():
            if wall_selector.gid is not None:
                self._canvas.delete(wall_selector.gid)
                wall_selector.gid = None

        for obj in self._drawn_objects:
            obj.destroy()
        self._drawn_objects.clear()

    def _draw_bounding_box(self, y: int, height: int) -> int:
        """
        Draws a bounding box from y coordinate with a height. Width of the
        bounding box depends on margin.
        :return gui of created graphic object
        """
        rect = self._canvas.create_rectangle(
            self._leftmost_pos + PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN, y,
            self._rightmost_pos - PROPERTY_SETTINGS_BOUNDING_BOX_MARGIN,
            y + height, fill="#F5F5A8")
        self._drawn_ids.append(rect)
        return rect

    def destroy(self):
        self._delete_graphical_objects()
