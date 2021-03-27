import logging
from typing import Optional

import pytest

from game.gamemap import GameMap
from game.utils.direction import Direction
from game.utils.position import Position
from test.utils import loadMap

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.blocks.impl.player import Player
    from game.blocks.impl.duck_pool import DuckPoolBlock

logging.basicConfig(level=logging.DEBUG)


def _find_one_player(map: GameMap) -> Optional['Player']:
    players = list(map.getPlayers())
    if players is None or len(players) < 1:
        return None
    elif len(players) > 1:
        raise AssertionError("Found more than one player, but it was assumed there is only one")
    return players[0]


def test_empty_moveright():
    # Given
    map, manager = loadMap("test_empty.json")

    # When
    manager.move_all_players(Direction.RIGHT)

    # Then
    p = _find_one_player(map)
    print(type(p))
    assert not p.is_alive
    assert p.position == Position(4, 0)


def test_empty_moveleft():
    # Given
    map, manager = loadMap("test_empty.json")

    # When
    manager.move_all_players(Direction.LEFT)

    #Then
    p = _find_one_player(map)
    assert not p.is_alive
    assert p.position == Position(0, 0)


def test_stone_moveleft():
    # Given
    map, manager = loadMap("test_stone.json")

    # When
    manager.move_all_players(Direction.LEFT)

    # Then
    p = _find_one_player(map)
    assert p.position == Position(3, 0)

    # When
    manager.move_all_players(Direction.LEFT)

    # Then
    p = _find_one_player(map)
    assert p.position == Position(3, 0)
    assert p.is_alive


def test_stone_movearound():
    # Given
    map, manager = loadMap("test_stone_4x4.json")

    # When-Then
    manager.move_all_players(Direction.RIGHT)
    assert _find_one_player(map).position == Position(2, 1)
    manager.move_all_players(Direction.DOWN)
    assert _find_one_player(map).position == Position(2, 2)
    manager.move_all_players(Direction.LEFT)
    assert _find_one_player(map).position == Position(1, 2)
    manager.move_all_players(Direction.UP)
    assert _find_one_player(map).position == Position(1, 1)


def test_spike_moveup():
    # Given
    map, manager = loadMap("test_spike.json")

    # When
    manager.move_all_players(Direction.UP)

    # Then
    p = _find_one_player(map)
    assert p.position == Position(0, 3)
    assert not p.is_alive


def test_spike_moveup_directhit():
    # Given
    map, manager = loadMap("test_spike.json")
    p = _find_one_player(map)
    map.move(pos_from=Position(0, 5), pos_to=Position(0, 3), what=p)


    # When
    manager.move_all_players(Direction.UP)
    p = _find_one_player(map)

    # Then
    assert p.position == Position(0, 3)
    assert not p.is_alive


def test_spike_movedown():
    # Given
    map, manager = loadMap("test_spike.json")
    p = _find_one_player(map)
    map.move(pos_from=Position(0, 5), pos_to=Position(0, 1), what=p)

    # When
    manager.move_all_players(Direction.DOWN)

    # Then
    p = _find_one_player(map)
    assert p.position == Position(0, 1)
    assert p.is_alive


def test_melting_ice():
    # Given
    map, manager = loadMap("test_melting_ice.json")

    # When-Then
    manager.move_all_players(Direction.DOWN)
    p = _find_one_player(map)
    assert p.position == Position(0, 4)
    assert p.is_alive

    # When-Then
    manager.move_all_players(Direction.UP)
    manager.move_all_players(Direction.DOWN)
    p = _find_one_player(map)
    assert p.position == Position(0, 4)
    assert p.is_alive

    # When-Then
    manager.move_all_players(Direction.UP)
    manager.move_all_players(Direction.DOWN)
    p = _find_one_player(map)
    # Ice is now broken
    assert p.position == Position(0, 5)
    assert p.is_alive


def test_duckpool():
    # Given
    map, manager = loadMap("test_duckpool.json")

    # When
    manager.move_all_players(Direction.RIGHT)

    # Then
    assert _find_one_player(map) is None
    pool: DuckPoolBlock = map.block(Position(3, 0)).top()
    assert pool.capacity == -1
    assert pool.free_space == -1
    assert len(pool._blocks_in_pool) == 1
