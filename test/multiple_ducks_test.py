import pytest

from game.utils.direction import Direction
from game.utils.position import Position
from test.utils import loadMap

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.blocks.impl.player import Player


def test_two_ducks_move_in_row():
    # Given
    map, manager = loadMap("test_multi_ducks.json")

    # When
    manager.move_all_players(Direction.RIGHT)

    # Then
    p1: 'Player' = map.block(Position(4, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(5, 0)).top()
    assert p2.is_alive

    # When
    manager.move_all_players(Direction.LEFT)

    # Then
    p1: 'Player' = map.block(Position(1, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(2, 0)).top()
    assert p2.is_alive


def test_two_ducks_against_melting_ice():
    # Given
    map, manager = loadMap("test_multi_ducks_with_ice.json")

    # When
    manager.move_all_players(Direction.RIGHT)

    # Then
    p1: 'Player'= map.block(Position(4, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(5, 0)).top()
    assert p2.is_alive
