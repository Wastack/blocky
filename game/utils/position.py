from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, o):
        return Position(x=self.x + o.x, y=self.y + o.y)

    def __str__(self) -> str:
        return f"P({self.x}, {self.y})"