from dataclasses import dataclass
from typing import List

from game.utils.position import Position

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
BLOCK_SIZE = 50


def rect_from_pos(pos: Position, size=BLOCK_SIZE) -> List[int]:
    rect = [pos.x * size, pos.y * size,
            pos.x * size + size, pos.y * size + size,
            ]
    return rect


@dataclass
class MouseRange:
    x1: int
    y1: int
    x2: int
    y2: int

    def contains(self, x:int, y:int):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

