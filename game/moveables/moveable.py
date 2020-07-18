from abc import ABC, abstractmethod

from game.utils.direction import Direction


class Moveable(ABC):

    @property
    @abstractmethod
    def direction(self) -> Direction:
        pass

    def set_dead(self, _is_dead=True):
        pass

