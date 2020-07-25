from typing import List

from game.utils.position import Position

BLOCK_SIZE = 50


def rect_from_pos(pos: Position, size = BLOCK_SIZE) -> List[int]:
    rect = [pos.x * size, pos.y * size,
            pos.x * size + size, pos.y * size + size,
            ]
    return rect
