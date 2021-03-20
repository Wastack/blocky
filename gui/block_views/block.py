import abc
import os
import tkinter
from abc import ABC
from tkinter.font import Font
from typing import Any, Optional

from PIL import Image, ImageTk

from game.blocks.block import AbstractBlock
from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block_capability import BlockCapability
from gui.imageFactory import ImageFactory
from gui.utils import rect_from_pos, BLOCK_SIZE


class BlockView(ABC):
    def __init__(self, canvas: tkinter.Canvas, block_fill_color="wheat1"):
        self._canvas = canvas
        self._rect: Optional[int] = None
        self._img: Optional[tkinter.Label] = None
        self._block_color = block_fill_color
        self._block = self._set_default_block()
        self._png_file_name = ""

    def _create_block(self, pos: Position) -> Any:
        rect = rect_from_pos(pos)
        return self._canvas.create_rectangle(*rect, fill=self._block_color)

    def _create_text(self, pos: Position, text: str) -> int:
        times = Font(family="Times", size=str(BLOCK_SIZE // 2), weight="bold")
        text_id = self._canvas.create_text(pos.x * BLOCK_SIZE + BLOCK_SIZE // 2, pos.y * BLOCK_SIZE + BLOCK_SIZE // 2 + 2, text=text, fill="DeepSkyBlue4", font=times)
        return text_id

    def draw(self, pos: Position) -> Any:
        if self._rect is not None:
            self.destroy()

        if self._png_file_name != "":
            img_factory = ImageFactory()
            photo = img_factory.get_image(self._png_file_name)
            self._img = self._canvas.create_image(pos.x*BLOCK_SIZE + BLOCK_SIZE // 2, pos.y*BLOCK_SIZE + BLOCK_SIZE // 2, image=photo)
        self._rect = self._create_block(pos)
        self._canvas.tag_lower(self._rect)
        return self._rect

    def destroy(self):
        for canvas_obj in [self._rect, self._img]:
            if canvas_obj is not None:
                self._canvas.delete(canvas_obj)

        self._rect = None
        self._img = None

    def set_wall(self, side: Direction, wall_view: Optional[Wall]):
        pass

    def _set_png_image(self, png_file_name: str):
        self._png_file_name = png_file_name

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

    @property
    def game_block(self) -> AbstractBlock:
        return self._block

    @abc.abstractmethod
    def _set_default_block(self) -> AbstractBlock:
        raise NotImplementedError()