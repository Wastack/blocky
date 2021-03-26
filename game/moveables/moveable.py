import abc
from abc import ABC, abstractmethod

from game.utils.direction import Direction


class Moveable(ABC):

    @abc.abstractmethod
    def set_dead(self, _is_dead=True):
        pass

    @property
    @abc.abstractmethod
    def is_alive(self) -> bool:
        pass