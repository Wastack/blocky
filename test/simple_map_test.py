import logging
from typing import Tuple

import pytest

from game.blocks.impl.player import Player
from game.gamemap import GameMap
from game.utils.direction import Direction
from game.utils.position import Position
from test.utils import loadMap

logging.basicConfig(level=logging.DEBUG)


def _find_player(map: GameMap) -> Tuple[Player, Position]:
    return map.getPlayers()[0]

def test_empty_moveright():
    # Given
    map, manager = loadMap("test_empty.json")

    # When
    manager.move_all_players(Direction.RIGHT)

    # Then
    p, pos = _find_player(map)
    assert not p.is_alive()
    assert pos == Position(4, 0)


def test_empty_moveleft():
    # Given
    map, manager = loadMap("test_empty.json")

    # When
    manager.move_all_players(Direction.LEFT)

    #Then
    p, pos = _find_player(map)
    assert not p.is_alive()
    assert pos == Position(0, 0)


def test_stone_moveleft():
    # Given
    map, manager = loadMap("test_stone.json")

    # When
    manager.move_all_players(Direction.LEFT)

    # Then
    p, pos = _find_player(map)
    assert pos == Position(3, 0)

    # When
    manager.move_all_players(Direction.LEFT)

    # Then
    p, pos = _find_player(map)
    assert pos == Position(3, 0)
    assert p.is_alive()


def test_stone_movearound():
    # Given
    map, manager = loadMap("test_stone_4x4.json")

    # When-Then
    manager.move_all_players(Direction.RIGHT)
    assert _find_player(map)[1] == Position(2, 1)
    manager.move_all_players(Direction.DOWN)
    assert _find_player(map)[1] == Position(2, 2)
    manager.move_all_players(Direction.LEFT)
    assert _find_player(map)[1] == Position(1, 2)
    manager.move_all_players(Direction.UP)
    assert _find_player(map)[1] == Position(1, 1)


def test_spike_moveup():
    # Given
    map, manager = loadMap("test_spike.json")

    # When
    manager.move_all_players(Direction.UP)

    # Then
    p, pos = _find_player(map)
    assert pos == Position(0, 3)
    assert not p.is_alive()


def test_spike_moveup_directhit():
    # Given
    map, manager = loadMap("test_spike.json")
    p, _ = _find_player(map)
    map.move(pos_from=Position(0, 5), pos_to=Position(0, 3), what=p)


    # When
    manager.move_all_players(Direction.UP)
    p, pos = _find_player(map)

    # Then
    assert pos == Position(0, 3)
    assert not p.is_alive()


def test_spike_movedown():
    # Given
    map, manager = loadMap("test_spike.json")
    p, _ = _find_player(map)
    map.move(pos_from=Position(0, 5), pos_to=Position(0, 1), what=p)

    # When
    manager.move_all_players(Direction.DOWN)

    # Then
    p, pos = _find_player(map)
    assert pos == Position(0, 1)
    assert p.is_alive()
