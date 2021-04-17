import asyncio
import json
import logging
import os
import pathlib

import aiofiles as aiofiles
import websockets

from game.gamemap import GameMap
from game.json_import.map_schema import MapSchema
from game.utils.direction import Direction

FORMAT = "[%(levelname)5s - %(filename)s:%(lineno)s::%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.getLogger("PIL").setLevel(logging.WARNING)


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


async def receive_move(websocket):
    message: str = await websocket.recv()
    direction = Direction[message.upper()]
    logging.debug(f"Direction received: {direction}")


async def hello(websocket, _path: str):
    logging.info("Received connection")

    # Parse map
    map_model = await open_map("boulder.json")

    # Send map
    schema = MapSchema()
    back_to_json = schema.dumps(map_model)
    await websocket.send(back_to_json)

    # Wait for user input
    while True:
        await receive_move(websocket)


def main():
    HOST, PORT = "localhost", 8765
    start_server = websockets.serve(hello, HOST, PORT)
    logging.info(f"Serving at {HOST}:{PORT}")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
