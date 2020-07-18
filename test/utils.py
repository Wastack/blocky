import json
import os
import pathlib
from typing import Tuple

from game.gamemap import GameMap
from game.json_import.map_schema import MapSchema
from game.player_manager import PlayerManager


def loadMap(json_filename: str) -> Tuple[GameMap, PlayerManager]:
    with open(os.path.join(pathlib.Path(__file__).parent ,"data", json_filename)) as fp:
        json_data = json.load(fp)
        schema = MapSchema()
        my_map = schema.load(json_data)
        return (my_map, PlayerManager(my_map))
