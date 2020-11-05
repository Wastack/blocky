import abc
import tkinter
from abc import ABC
from tkinter.font import Font
from typing import Any, Optional, List

from game.blocks.block import AbstractBlock
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block_capability import BlockCapability
from gui.block_views.wall_views.wall_view import WallView
from gui.utils import rect_from_pos, BLOCK_SIZE


class BlockView(ABC):
    def __init__(self, canvas: tkinter.Canvas):
        self._canvas = canvas
        self._rect: Optional[int] = None

    def _create_block(self, pos: Position) -> Any:
        rect = rect_from_pos(pos)
        return self._canvas.create_rectangle(*rect, fill="wheat1")

    def _create_text(self, pos: Position, text: str) -> int:
        times = Font(family="Times", size=str(BLOCK_SIZE // 2), weight="bold")
        text_id = self._canvas.create_text(pos.x * BLOCK_SIZE + BLOCK_SIZE // 2, pos.y * BLOCK_SIZE + BLOCK_SIZE // 2 + 2, text=text, fill="DeepSkyBlue4", font=times)
        return text_id

    def draw(self, pos: Position) -> Any:
        if self._rect is not None:
            self.destroy()
        self._rect = self._create_block(pos)
        self._canvas.tag_lower(self._rect)
        return self._rect

    def destroy(self):
        self._canvas.delete(self._rect)
        self._rect = None

    def set_wall(self, side: Direction, wall_view: WallView):
        pass

    @staticmethod
    def block_capability() -> BlockCapability:
        return BlockCapability()

    @staticmethod
    @abc.abstractmethod
    def repr() -> str:
        return "????"

    @staticmethod
    @abc.abstractmethod
    def from_block(canvas: tkinter.Canvas, block) -> Optional['BlockView']:
        return

    @abc.abstractmethod
    def to_game_block(self) -> AbstractBlock:
        pass
