

class Position:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

    def __eq__(self, o: 'Position'):
        return (self.x == o.x) and (self.y == o.y)

    def __add__(self, o):
        return Position(x=self.x + o.x, y=self.y + o.y)

    def __str__(self) -> str:
        return f"P({self.x}, {self.y})"