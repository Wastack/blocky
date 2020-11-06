import logging
from tkinter import Canvas
from typing import Type, Optional

from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views.block import BLOCK_SIZE, BlockView
from gui.block_views.wall_views.empty_wall_view import EmptyWallView
from gui.block_views.wall_views.wall_view import WallView
from gui.controllers.selection_controller import SelectionController
from gui.utils import MouseRange
from gui.views.map_view import MapView


class BlockSelectionController(SelectionController):
    def __init__(self, canvas: Canvas, map_view: MapView):
        super().__init__(canvas)
        self._map = map_view
        self._exceptions = {}

        self._head: Optional[Position] = None

    def set_exception(self, mouse_range: MouseRange, key: str, enable_shift_select=False):
        self._exceptions[key] = (mouse_range, enable_shift_select)

    def _in_exception(self, x, y, shift_candidate: bool = False) -> bool:
        """
        Check if mouse position is in exception
        :param x: x mouse position
        :param y: y mouse position
        :param shift_candidate: whether mouse position is a part of a range selection or not.
        :return: Whether block can be selected or not.
        """
        if shift_candidate:
            ranges = [v for v, shift_enabled in self._exceptions.values() if not shift_enabled]
        else:
            ranges = [v for v, _ in self._exceptions.values()]
        return any([e.contains(x, y) for e in ranges])

    def _game_pos_in_exception(self, p: Position, shift_candidate: bool = False):
        """Check if a block intersects with an exception"""
        left_most = p.x * BLOCK_SIZE, p.y*BLOCK_SIZE
        bottom_right = left_most[0]+BLOCK_SIZE, left_most[1]+BLOCK_SIZE
        return self._in_exception(*left_most, shift_candidate=shift_candidate) \
            or self._in_exception(*bottom_right, shift_candidate=shift_candidate)

    def _select_game_pos(self, pos: Position):
        # Block outside of game map is not selectable
        if not self._map.size.contains(pos):
            return

        self._set_selection((pos.x*BLOCK_SIZE, pos.y*BLOCK_SIZE), BLOCK_SIZE, pos)

    @staticmethod
    def _mouse_pos_to_game_pos(x, y) -> Position:
        return Position(x // BLOCK_SIZE, y // BLOCK_SIZE)

    def _shift_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return

        # If no selections were made yet, shift click works pretty much like simple click
        if self._head is None:
            self._clicked(mouse_event)
            return

        pos = BlockSelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        for x in range(min(pos.x, self._head.x), max(pos.x, self._head.x) + 1):
            for y in range(min(pos.y, self._head.y), max(pos.y, self._head.y) + 1):
                p = Position(x, y)
                if self._game_pos_in_exception(p, shift_candidate=True):
                    continue
                self._select_game_pos(p)
        self._head = pos

    def _control_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        pos = BlockSelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._select_game_pos(pos)
        self._head = pos

    def _clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        self.deselect_all()
        self._control_clicked(mouse_event)
    
    def put_block_to_selection(self, block_type: Type[BlockView]) -> None:
        logging.info("Put block to selection event triggered.")
        if not self.has_selection():
            return
        for pos in self.selected_items:
            self._map.replace_at(pos, block_type(self._canvas))

    def put_wall_to_selection(self, side: Direction, wall_type: Type[WallView]) -> None:
        logging.info("Put wall to selection event triggered.")
        if not self.has_selection():
            return
        for pos in self.selected_items:
            for block in self._map.cell(pos):
                if wall_type in block.block_capability().possible_wall_types or wall_type == EmptyWallView:
                    block.set_wall(side, wall_type(self._canvas, side))
        self._map.draw()
