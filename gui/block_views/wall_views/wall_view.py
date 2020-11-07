import tkinter
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

from game.blocks.walls.wall import Wall, WallContainer
from game.utils.direction import Direction
from game.utils.position import Position
from gui.utils import BLOCK_SIZE

WALL_WIDTH = 4

class WallView(ABC):

    @abstractmethod
    def __init__(self, canvas, direction: Direction):
        pass

    @staticmethod
    def calc_real_pos(pos: Position, d: Direction) -> ((int, int), (int, int)):
        """
        Calculates line section in real coordinates represented by two points
        """
        if d == Direction.LEFT or d == Direction.UP:
            # Beginning from top left corner
            p1 = (pos.x * BLOCK_SIZE + WALL_WIDTH//2, pos.y * BLOCK_SIZE + WALL_WIDTH//2)
        else:
            # Beginning from bottom right corner
            p1 = ((pos.x+1) * BLOCK_SIZE - WALL_WIDTH//2, (pos.y+1) * BLOCK_SIZE - WALL_WIDTH//2)
        if d == Direction.LEFT or d == Direction.DOWN:
            # Until bottom left corner
            p2 = (pos.x * BLOCK_SIZE + WALL_WIDTH//2, (pos.y+1) * BLOCK_SIZE - WALL_WIDTH//2)
        else:
            # Until top right corner
            p2 = ((pos.x + 1) * BLOCK_SIZE - WALL_WIDTH//2, pos.y * BLOCK_SIZE + WALL_WIDTH//2)
        return p1, p2

    @staticmethod
    def to_wall_container(wall_view_dict: Dict[Direction, 'WallView']):
        params = {}
        for side, wall_view in wall_view_dict.items():
            if wall_view is None:
                continue
            params[side.value] = wall_view.to_game_wall()
        return WallContainer(**params)

    @staticmethod
    @abstractmethod
    def from_wall(canvas: tkinter.Canvas, wall: Wall,
                  direction: Direction) -> Optional['WallView']:
        return

    @abstractmethod
    def to_game_wall(self) -> Wall:
        pass

    @abstractmethod
    def draw(self, pos: Position) -> Any:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def repr() -> str:
        return "?????"
