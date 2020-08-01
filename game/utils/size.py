from dataclasses import dataclass


@dataclass
class Size():
    height: int
    width: int

    def __iter__(self):
        return (self.width, self.height).__iter__()

