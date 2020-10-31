from dataclasses import dataclass
from enum import Enum
import platform
from typing import List

from game.utils.position import Position

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
BLOCK_SIZE = 50


class ButtonEventType(Enum):
    CLICK = "Button"
    RELEASE = "ButtonRelease"


def tkinter_right_mouse_button(button_event_type: ButtonEventType) -> str:
    # On Mac right mouse button is signed by 2 instead of 3
    right_mouse_id = "2" if platform.system() == "Darwin" else "3"

    return f"<{button_event_type.value}-{right_mouse_id}>"


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

