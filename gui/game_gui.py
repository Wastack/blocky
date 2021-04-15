import functools
import logging
from typing import Callable, Any

from game.gamemap import GameMap
from game.player_manager import PlayerManager
from game.utils.direction import Direction
from gui.views.map_view import MapView


class GameGUI:
    def __init__(self, canvas, game_map: GameMap):
        self._canvas = canvas
        self._map_view = MapView(game_map=game_map, canvas=canvas)
        self._game_over_callback = None

    def draw(self):
        self._map_view.draw()

    def destroy(self):
        self._map_view.destroy()

    def register_game_events(self, callback: Callable[[],None]):
        self._game_over_callback = callback
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            event_name = f"<{direction.value.title()}>"
            logging.info(f"Register move event: {event_name}")
            self._canvas.bind(event_name, functools.partial(self._move_player, direction))
        self._canvas.bind("<Escape>", self._exit)

    def _move_player(self, direction: Direction, *args):
        logging.info(f"Move event received. Direction: {direction}")
        player_manager = PlayerManager(self._map_view.game_map)
        player_manager.execute_turn(direction)
        self._map_view.draw()

    def unregister_game_events(self):
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT,
                          Direction.RIGHT]:
            event_name = f"<{direction.value.title()}>"
            logging.info(f"Unregister move event: {event_name}")
            self._canvas.unbind(event_name)
        self._canvas.unbind("<Escape>")

    def _exit(self, *args):
        self.unregister_game_events()
        self.destroy()
        if self._game_over_callback is not None:
            self._game_over_callback()