import logging
import tkinter
from typing import Any, Optional

from game.blocks.walls.killer_wall import KillerWall
from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.wall_views.wall_view import WallView


class SpikeView(WallView):
    def __init__(self, canvas: tkinter.Canvas, d: Direction):
        self._canvas = canvas
        self._direction = d
        self._wall_id = None

    @staticmethod
    def from_wall(canvas: tkinter.Canvas, wall,
                  direction: Direction) -> Optional['WallView']:
        if not isinstance(wall, KillerWall):
            return None
        return SpikeView(canvas, direction)

    def draw(self, pos: Position) -> Any:
        p1, p2 = WallView.calc_real_pos(pos, self._direction)
        self._wall_id = self._canvas.create_line(*p1, *p2, width=6, fill="red")
        logging.debug("Rock block drawn")
        return self._wall_id

    def destroy(self) -> None:
        if self._wall_id:
            logging.debug("Spike destroyed")
            self._canvas.delete(self._wall_id)
        self._wall_id = None

    @staticmethod
    def repr() -> str:
        return "Spike"

    def to_game_wall(self) -> Wall:
        return KillerWall()