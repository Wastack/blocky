import pytest

from game.blocks.impl.boulder import Boulder
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
    manager.execute_turn(Direction.RIGHT)

    # Then
    p1: 'Player' = map.block(Position(4, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(5, 0)).top()
    assert p2.is_alive

    # When
    manager.execute_turn(Direction.LEFT)

    # Then
    p1: 'Player' = map.block(Position(1, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(2, 0)).top()
    assert p2.is_alive


def test_two_ducks_against_melting_ice():
    # Given
    map, manager = loadMap("test_multi_ducks_with_ice.json")

    # When
    manager.execute_turn(Direction.RIGHT)

    # Then
    p1: 'Player'= map.block(Position(4, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(5, 0)).top()
    assert p2.is_alive

def test_duck_boulder_duck():
    # Given
    map, manager = loadMap("test_duck_boulder_duck.json")

    # When
    manager.execute_turn(Direction.RIGHT)

    # Then
    p1: 'Player'= map.block(Position(3, 0)).top()
    assert p1.is_alive
    p2: 'Player' = map.block(Position(5, 0)).top()
    assert p2.is_alive
    assert type(map.block(Position(4, 0)).top()) == Boulder


def test_multiple_frogs():
    # Given
    map, manager = loadMap("test_multiple_frogs.json")

    # When
    manager.execute_turn(Direction.RIGHT)

    # Then
    p: 'Player' = map.block(Position(2, 0)).top()
    assert p.is_alive
    p = map.block(Position(3, 0)).top()
    assert p.is_alive
    p = map.block(Position(4, 0)).top()
    assert p.is_alive

    # When
    manager.execute_turn(Direction.RIGHT)

    # Then
    p: 'Player' = map.block(Position(3, 0)).top()
    assert p.is_alive
    p = map.block(Position(4, 0)).top()
    assert p.is_alive
    p = map.block(Position(5, 0)).top()
    assert p.is_alive

    # When
    manager.execute_turn(Direction.LEFT)

    # Then
    p: 'Player' = map.block(Position(1, 0)).top()
    assert p.is_alive
    p = map.block(Position(3, 0)).top()
    assert p.is_alive
    p = map.block(Position(4, 0)).top()
    assert p.is_alive
