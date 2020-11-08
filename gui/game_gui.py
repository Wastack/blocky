import functools
import logging

from game.player_manager import PlayerManager
from game.utils.direction import Direction
from gui.views.map_view import MapView


class GameGUI:
    def __init__(self, canvas, map_view: MapView):
        self._canvas = canvas
        self._map_view = map_view
        self.game_model = map_view.to_game_map()

    def register_game_events(self):
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            # First letter needs to be capitalized
            event_name = f"<{direction.value.title()}>"
            logging.info(f"Register move event: {event_name}")
            self._canvas.bind(event_name, functools.partial(self._move_player, direction))

    def _move_player(self, direction: Direction, *args):
        logging.info(f"Move event received. Direction: {direction}")
        player_manager = PlayerManager(self.game_model)
        player_manager.move_all_players(direction)
        new_map_view = MapView(game_map=self.game_model, canvas=self._canvas)
        new_map_view.draw()
        self._map_view.destroy()
        self._map_view = new_map_view
