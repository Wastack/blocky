import logging

from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from gui.block_views.wall_views.spike import SpikeView
from gui.block_views.wall_views.wall_view import WallView

registered_wall_views = [
    SpikeView,
]


def from_wall(wall: Wall, d: Direction, canvas) -> WallView:
    for canditate_type in registered_wall_views:
        candidate = canditate_type.from_wall(canvas, wall, d)
        if candidate is not None:
            return candidate
    logging.error(f"No registered wall view is found for wall of type: {type(wall)}")
    raise RuntimeError("block view factory failed")
