import asyncio
import json
import logging
import os
import pathlib
from typing import Optional

import aiofiles as aiofiles
import websockets

from game.gamemap import GameMap
from game.json_import.map_schema import MapSchema
from game.json_import.reports_schema import TurnSchema
from game.player_manager import PlayerManager
from game.utils.direction import Direction

FORMAT = "[%(levelname)5s - %(filename)s:%(lineno)s::%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.getLogger("PIL").setLevel(logging.WARNING)

class WebGame:
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__map_model: Optional[GameMap] = None
        self.__player_manager: Optional[PlayerManager] = None

    async def __send_map(self, websocket):
        schema = MapSchema()
        back_to_json = schema.dumps(self.__map_model)
        await websocket.send(back_to_json)

    @staticmethod
    async def open_map(file_name: str) -> GameMap:
        # Load a test data for debugging
        async with aiofiles.open(
                os.path.join(pathlib.Path(__file__).parent.parent, "example_maps",
                             file_name)) as fp:
            data = await fp.read()
            json_data = json.loads(data)

        schema = MapSchema()
        map_model = schema.load(json_data)

        return map_model

    async def receive_move(self, websocket):
        message: str = await websocket.recv()
        direction = Direction[message.upper()]
        logging.debug(f"Direction received: {direction}")

        steps = self.__player_manager.execute_turn(direction)

        turn_result = {
            "steps" : steps,
            "map_result" : self.__map_model,
        }
        schema = TurnSchema()
        msg = schema.dumps(turn_result)
        await websocket.send(msg)

    async def hello(self, websocket, _path: str):
        logging.info("Received connection")

        # Parse map
        self.__map_model = await self.open_map("boulder.json")
        self.__player_manager = PlayerManager(self.__map_model)

        # Send map
        await self.__send_map(websocket)

        # Wait for user input
        while True:
            await self.receive_move(websocket)

    def main(self):
        start_server = websockets.serve(self.hello, self.__host, self.__port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    game = WebGame(host="localhost", port=8765)
    game.main()
