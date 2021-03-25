import logging
from tkinter import Canvas
from typing import Type, Optional, Callable, Any

from game.blocks.impl.duck_pool import DuckPoolBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.blocks.walls.wall import Wall
from game.utils.direction import Direction
from game.utils.position import Position
from gui.block_views import block_view_factory
from gui.block_views.block import BLOCK_SIZE, BlockView
from gui.controllers.selection_controller import SelectionController
from gui.utils import MouseRange
from gui.views.map_view import MapView


def _with_redraw(func):
    def wrap(self: SelectionController, *args):
        func(self, *args)
        self._map.draw()
    return wrap


class BlockSelectionController(SelectionController):
    def __init__(self, canvas: Canvas, map_view: MapView):
        super().__init__(canvas)
        self._map = map_view
        self._exceptions = {}

        self._head: Optional[Position] = None
        self._changed_callbacks = []

    def subscribe_changed(self, callback: Callable[[],Any]):
        self._changed_callbacks.append(callback)

    def on_changed(self):
        for c in self._changed_callbacks:
            c()

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
        self.on_changed()

    def _control_clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        pos = BlockSelectionController._mouse_pos_to_game_pos(mouse_event.x, mouse_event.y)
        self._select_game_pos(pos)
        self._head = pos
        self.on_changed()

    def _clicked(self, mouse_event):
        if self._in_exception(mouse_event.x, mouse_event.y):
            return
        self.deselect_all()
        self._control_clicked(mouse_event)

    @_with_redraw
    def put_block_to_selection(self, block_type: Type[BlockView]) -> None:
        logging.info("Put block to selection event triggered.")
        if not self.has_selection():
            return
        for pos in self.selected_items:
            # There is always a default constructor
            self._map.replace_at(pos, block_view_factory.to_block(block_type))

    @_with_redraw
    def put_wall_to_selection(self, side: Direction, wall: Optional[Wall]) -> None:
        logging.info("Put wall to selection event triggered.")
        if not self.has_selection():
            return
        for pos in self.selected_items:
            block = self._map.cell(pos)
            wallContainer = block.walls()
            if wallContainer is not None:
                wallContainer.set_side(wall, side)

    @_with_redraw
    def change_capacity_on_selection(self, capacity: int):
        logging.debug("Change capacity on selected blocks")
        if not self.has_selection():
            logging.debug("No blocks selected to change capacity on")
            return
        for pos in self.selected_items:
            block = self._map.cell(pos)
            if isinstance(block, MeltingIceBlock) and capacity > 0:
                block.set_life(capacity)
            elif isinstance(block, DuckPoolBlock) and capacity >= -1:
                block.set_capacity(capacity)