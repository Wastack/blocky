import tkinter
from typing import Any, Optional

from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.wall_views.wall_view import WallView


class EmptyWallView(WallView):
    def __init__(self, _canvas: tkinter.Canvas, _d: Direction):
        pass

    @staticmethod
    def from_wall(canvas: tkinter.Canvas, wall,
                  direction: Direction) -> Optional['WallView']:
        return None

    def draw(self, pos: Position) -> Any:
        pass

    def destroy(self) -> None:
        pass

    @staticmethod
    def repr() -> str:
        return "Empty"

    def to_game_wall(self) -> Wall:
        return None
