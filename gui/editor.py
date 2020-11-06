import json
import logging
import os
import pathlib
import tkinter

from game.json_import.map_schema import MapSchema
from gui.block_views.block_view_factory import registered_block_views
from gui.utils import WINDOW_WIDTH, WINDOW_HEIGHT
from gui.views.map_view import MapView
from gui.views.property_settings import PropertySettings
from gui.views.resizer import Resizer
from gui.controllers.block_selection_controller import BlockSelectionController
from gui.views.palette import Palette


FORMAT = "[%(levelname)5s - %(filename)s:%(lineno)s::%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class EditorGUI:
    def __init__(self):
        pass

    def show(self):
        self._create_window()
        self._create_game_canvas()
        self._create_menu()

        # Waiting for events. Blocks the execution
        self._window.mainloop()

    def _create_window(self) -> None:
        logging.info("Create window")
        self._window = tkinter.Tk()
        self._window.title("Blocky")
        # window.attributes('-fullscreen', True)
        self._window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def _create_game_canvas(self) -> None:
        logging.info("Create editor canvas")
        canvas = tkinter.Canvas(self._window)
        canvas.configure(bg="black")
        canvas.pack(fill="both", expand=True, side="left")

        with open(
                os.path.join(pathlib.Path(__file__).parent.parent, "test/data",
                             "test_spike.json")) as fp:
            json_data = json.load(fp)
        schema = MapSchema()
        my_map = schema.load(json_data)
        map_view = MapView(my_map, canvas)
        map_view.draw()

        selection_controller = BlockSelectionController(canvas, map_view)
        selection_controller.register_canvas_events(click=True, shift=True,
                                                    control=True)

        resizer = Resizer(canvas, map_view, selection_controller,
                          map_view.resize)
        resizer.draw_resizing_rect()

        palette_controller = Palette(canvas, registered_block_views)
        palette_controller.register_right_mouse(
            selection_controller.put_block_to_selection)

        settings_canvas = tkinter.Canvas(self._window, bg="black", width=200)
        settings_canvas.pack(side="right", fill="y")
        property_settings = PropertySettings(settings_canvas,
                                             selection_controller)
        property_settings.draw_settings_window()

    def _create_menu(self):
        logging.info("Create window menu")
        menu_bar = tkinter.Menu(self._window)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self._edit_new_map)
        file_menu.add_command(label="Open", command=self._open_map)
        file_menu.add_command(label="Save", command=self._save_map)
        file_menu.add_command(label="Save as...", command=self._save_map_as)

        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=self._window.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        edit_menu = tkinter.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")

        edit_menu.add_separator()

        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        edit_menu.add_command(label="Delete")
        edit_menu.add_command(label="Select All")

        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index")
        help_menu.add_command(label="About...")
        menu_bar.add_cascade(label="Help")
        self._window.config(menu=menu_bar)

    def _edit_new_map(self):
        raise NotImplementedError()

    def _open_map(self):
        raise NotImplementedError()

    def _save_map(self):
        raise NotImplementedError()

    def _save_map_as(self):
        raise NotImplementedError()


def main():
    editor = EditorGUI()
    editor.show()


if __name__ == "__main__":
    main()