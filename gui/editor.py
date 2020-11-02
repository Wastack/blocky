import json
import logging
import os
import pathlib
import tkinter
from typing import Any

from game.json_import.map_schema import MapSchema
from gui.block_views.block_view_factory import registered_block_views
from gui.utils import WINDOW_WIDTH, WINDOW_HEIGHT
from gui.views.map_view import MapView
from gui.views.property_settings import PropertySettings
from gui.views.resizer import Resizer
from gui.controllers.block_selection_controller import BlockSelectionController
from gui.views.palette import Palette


logging.basicConfig(level=logging.DEBUG)


def _create_window() -> tkinter.Tk:
    window = tkinter.Tk()
    window.title("Blocky")
    #window.attributes('-fullscreen', True)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    return window


def _create_game_canvas(window) -> tkinter.Canvas:
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True, side="left")

    with open(os.path.join(pathlib.Path(__file__).parent.parent ,"test/data", "test_spike.json")) as fp:
        json_data = json.load(fp)
    schema = MapSchema()
    my_map = schema.load(json_data)
    map_view = MapView(my_map, canvas)
    map_view.draw()

    selection_controller = BlockSelectionController(canvas, map_view)
    selection_controller.register_canvas_events(click=True, shift=True, control=True)

    resizer = Resizer(canvas, map_view, selection_controller, map_view.resize)
    resizer.draw_resizing_rect()

    palette_controller = Palette(canvas, registered_block_views)
    palette_controller.register_right_mouse(selection_controller.put_block_to_selection)

    settings_canvas = tkinter.Canvas(window, bg="black", width=200)
    settings_canvas.pack(side="right", fill="y")
    property_settings = PropertySettings(settings_canvas, selection_controller)
    property_settings.draw_settings_window()


def main():
    window = _create_window()
    _create_game_canvas(window)
    window.mainloop()


if __name__ == "__main__":
    main()