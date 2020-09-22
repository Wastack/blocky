import json
import logging
import os
import pathlib
import tkinter

from game.json_import.map_schema import MapSchema
from gui.utils import WINDOW_WIDTH, WINDOW_HEIGHT
from gui.views.map_view import MapView
from gui.views.property_settings import PropertySettings
from gui.views.resizer import Resizer
from gui.views.selection_controller import SelectionController
from gui.views.palette import Palette


logging.basicConfig(level=logging.DEBUG)

def _create_window() -> tkinter.Tk:
    window = tkinter.Tk()
    window.title("Blocky")
    #window.attributes('-fullscreen', True)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    return window


def _create_canvas(window) -> tkinter.Canvas:
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)

    with open(os.path.join(pathlib.Path(__file__).parent.parent ,"test/data", "test_spike.json")) as fp:
        json_data = json.load(fp)
    schema = MapSchema()
    my_map = schema.load(json_data)
    map_view = MapView(my_map, canvas)
    map_view.draw()

    selection_controller = SelectionController(canvas, map_view)
    selection_controller.register_canvas_events()

    resizer = Resizer(canvas, map_view, selection_controller, map_view.resize)
    resizer.draw_resizing_rect()

    palette_controller = Palette(canvas)
    palette_controller.register_right_mouse(selection_controller.put_block_to_selection)

    property_settings = PropertySettings(canvas)
    property_settings.draw_settings_window()

    return canvas


def main():
    window = _create_window()
    canvas = _create_canvas(window)
    window.mainloop()


if __name__ == "__main__":
    main()