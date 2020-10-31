from dataclasses import dataclass

from game.utils.position import Position


@dataclass
class Size():
    height: int
    width: int

    def __iter__(self):
        return (self.width, self.height).__iter__()

    def contains(self, p: Position):
        """Check if p position is inside the [0:0; width:height] interval"""
        return p.x < self.width and p.y < self.height
