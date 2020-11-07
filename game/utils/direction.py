from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    DEFAULT = "default"

    @staticmethod
    def opposite(d: 'Direction') -> 'Direction':
        if d == Direction.UP:
            return Direction.DOWN
        elif d == Direction.DOWN:
            return Direction.UP
        elif d == Direction.LEFT:
            return Direction.RIGHT
        elif d == Direction.RIGHT:
            return Direction.LEFT
        return Direction.DEFAULT
