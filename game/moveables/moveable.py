from abc import ABC, abstractmethod

from game.utils.direction import Direction


class Moveable(ABC):

    def set_dead(self, _is_dead=True):
        pass

