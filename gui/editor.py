import json
import logging
import os
import pathlib
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from typing import Optional

from game.gamemap import GameMap
from game.json_import.map_schema import MapSchema
from game.utils.size import Size
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
        self._game_canvas = None
        self._game_map: Optional[MapView] = None
        self._resizer: Resizer = None
        self._palette_controller = None
        self._selection_controller = None
        self._settings_canvas = None
        self._property_settings = None

    def show(self):
        self._create_window()

        # Load a test data for debugging
        with open(
                os.path.join(pathlib.Path(__file__).parent.parent, "test/data",
                             "test_spike.json")) as fp:
            json_data = json.load(fp)
        schema = MapSchema()
        map_model = schema.load(json_data)

        self._reset_canvas(map_model)
        self._create_menu()

        # Waiting for events. Blocks the execution
        self._window.mainloop()

    def _create_window(self) -> None:
        logging.info("Create window")
        self._window = tkinter.Tk()
        self._window.title("Blocky")
        # window.attributes('-fullscreen', True)
        self._window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def _reset_canvas(self, game_model: GameMap) -> None:
        """
        Resets the whole screen. It first creates the new widgets and destroy the previous afterwards.
        This behaviour prevents glitches.
        """
        logging.info("Reset game canvas")

        # Game Canvas
        if not self._game_canvas:
            self._game_canvas = tkinter.Canvas(self._window)
            self._game_canvas.configure(bg="black")
            self._game_canvas.pack(fill="both", expand=True, side="left")

        # Game Map
        gm = MapView(game_model, self._game_canvas)
        gm.draw()
        if self._game_map:
            self._game_map.destroy()
        self._game_map = gm

        # Selection Controller
        sc = BlockSelectionController(self._game_canvas, self._game_map)
        sc.register_canvas_events(click=True, shift=True,
                                                          control=True)
        if self._selection_controller:
            self._selection_controller.destroy()
        self._selection_controller = sc

        # Resizer (Controller)
        r = Resizer(self._game_canvas, self._game_map, self._selection_controller,
                    self._game_map.resize)
        r.draw_resizing_rect()
        if self._resizer:
            self._resizer.destroy()
        self._resizer = r

        # Palette Controller
        pc = Palette(self._game_canvas, registered_block_views)
        pc.register_right_mouse(self._selection_controller.put_block_to_selection)
        if self._palette_controller:
            self._palette_controller.destroy()
        self._palette_controller = pc

        # Settings canvas
        if not self._settings_canvas:
            self._settings_canvas = tkinter.Canvas(self._window, bg="black", width=200)
            self._settings_canvas.pack(side="right", fill="y")

        # Property Settings (Controller)
        ps = PropertySettings(self._settings_canvas,
                                             self._selection_controller)
        ps.draw_settings_window()
        if self._property_settings:
            self._property_settings.destroy()
        self._property_settings = ps

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
        if self._game_map is not None and (self._game_map.size.width > 1 or self._game_map.size.height > 1):
            # Warning/confirmation of lost data
            popup_result = tkinter.messagebox.askyesnocancel(title="Blocky", message="Current map is not saved. Wanna save it?")
            if popup_result is None:
                return
            if popup_result:
                # User wants to save file first.
                # TODO is it a save as?
                self._save_map_as()
        self._reset_canvas(GameMap(Size(1, 1)))

    def _open_map(self):
        raise NotImplementedError()

    def _save_map(self):
        raise NotImplementedError()

    def _save_map_as(self):
        if not self._game_map:
            err_msg = "Attempt to save when there is no game map loaded."
            logging.error(err_msg)
            raise RuntimeError(err_msg)
        schema = MapSchema()
        map_model = self._game_map.to_game_map()
        logging.debug(map_model)
        json_string = schema.dumps(map_model)
        with filedialog.asksaveasfile() as f:
            f.write(json_string)

    def _clear_game_canvas(self):
        if not self._game_canvas:
            return
        if self._game_map:
            self._game_map.destroy()
            self._game_map = None
        if self._selection_controller:
            self._selection_controller.destroy()
            self._selection_controller = None
        if self._palette_controller:
            self._palette_controller.destroy()
            self._palette_controller = None
        if self._resizer:
            self._resizer.destroy()
            self._resizer = None
        if self._property_settings:
            self._property_settings.destroy()
            self._property_settings = None


def main():
    editor = EditorGUI()
    editor.show()


if __name__ == "__main__":
    main()
