import logging
from typing import Dict, Any

from marshmallow import Schema, fields, post_load, validate, pre_dump
from marshmallow_oneofschema import OneOfSchema

from game.blocks.impl.duck_pool import DuckPoolBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.blocks.impl.player import Player
from game.blocks.impl.rock import RockBlock
from game.blocks.impl.boulder import Boulder
from game.blocks.walls.killer_wall import KillerWall
from game.blocks.walls.wall import WallContainer
from game.gamemap import GameMap
from game.utils.position import Position
from game.utils.size import Size


class PositionSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()

    @post_load
    def make_position(self, data, **kwargs) -> Position:
        return Position(**data)


class SpikeWallSchema(Schema):
    @post_load
    def make_spike(self, _data,  **kwargs) -> KillerWall:
        return KillerWall()

    @pre_dump
    def _pre_dump(self, _data, **kwargs):
        pass


class AbstractWallSchema(OneOfSchema):
    type_schemas = {
        "Spike": SpikeWallSchema,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, KillerWall):
            return "Spike"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class PlayerSchema(Schema):
    move_once = fields.Boolean(required=False)

    @post_load
    def make_player(self, data, **kwargs) -> Player:
        move_only_once = data.get("move_once", False)
        return Player(move_only_once=move_only_once)

    @pre_dump
    def _pre_dump(self, player_block: Player, **kwargs):
        return {"move_once": player_block.is_moving_only_once}


class RockSchema(Schema):
    walls = fields.Dict(keys=fields.String(validate=validate.OneOf(["down", "up", "right", "left"])),
                        values=fields.Nested(AbstractWallSchema), required=False)

    @post_load
    def post_load(self, data, **kwargs) -> RockBlock:
        if data.get("walls") is None:
            return RockBlock()
        return RockBlock(walls=WallContainer(**data["walls"]))

    @pre_dump
    def _pre_dump(self, rock_block: RockBlock, **kwargs):
        walls_dict = rock_block.walls().walls()
        result = {}
        for direction, val in walls_dict.items():
            if val is None:
                continue
            result[direction.value] = val
        if not result:
            return {}
        return {"walls": result}


class MeltingIceSchema(Schema):
    life = fields.Integer()
    walls = fields.Dict(keys=fields.String(validate=validate.OneOf(["down", "up", "right", "left"])),
                        values=fields.Nested(AbstractWallSchema), required=False)

    @post_load
    def post_load(self, data, **kwargs) -> MeltingIceBlock:
        life = data.get("life")
        life = life if life is not None else 1
        if data.get("walls") is None:
            return MeltingIceBlock(None, life)
        return MeltingIceBlock(life=life, walls=WallContainer(**data["walls"]))

    @pre_dump
    def _pre_dump(self, ice_block: MeltingIceBlock, **kwargs):
        walls_dict = ice_block.walls().walls()
        result = {}
        for direction, val in walls_dict.items():
            if val is None:
                continue
            result[direction.value] = val
        if not result:
            return {"life" : ice_block.life}
        return {"walls": result, "life": ice_block.life}


class DuckPoolSchema(Schema):
    capacity = fields.Integer()
    walls = fields.Dict(keys=fields.String(validate=validate.OneOf(["down", "up", "right", "left"])),
                        values=fields.Nested(AbstractWallSchema), required=False)

    @post_load
    def post_load(self, data, **kwargs) -> DuckPoolBlock:
        capacity = data.get("capacity")
        capacity = -1 if capacity is None else capacity
        if data.get("walls") is None:
            return DuckPoolBlock(None, capacity)
        return DuckPoolBlock(capacity=capacity, walls=WallContainer(**data["walls"]))

    @pre_dump
    def _pre_dump(self, duck_pool_block: DuckPoolBlock, **kwargs):
        walls_dict = duck_pool_block.walls().walls()
        result = {}
        for direction, val in walls_dict.items():
            if val is None:
                continue
            result[direction.value] = val
        if not result:
            return {"capacity": duck_pool_block.capacity}
        return {"walls": result, "capacity": duck_pool_block.capacity}


class RollingBlockSchema(Schema):

    @post_load
    def make_player(self, data, **kwargs) -> Boulder:
        return Boulder()


class AbstractBlockSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {
        "Anna": PlayerSchema,
        "Stone": RockSchema,
        "MeltingIce": MeltingIceSchema,
        "DuckPool": DuckPoolSchema,
        "RollingBlock" : RollingBlockSchema,
    }

    def get_obj_type(self, obj):
        # Order of isinstance is important: subclasses of more general classes
        # should be at front.
        obj_type = type(obj)
        if obj_type == Player:
            return "Anna"
        elif obj_type == MeltingIceBlock:
            return "MeltingIce"
        elif obj_type == DuckPoolBlock:
            return "DuckPool"
        elif obj_type == RockBlock:
            return "Stone"
        elif obj_type == Boulder:
            return "RollingBlock"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class MapSizeSchema(Schema):
    width = fields.Integer()
    height = fields.Integer()

    @post_load
    def make_map_size(self, data, **kwargs) -> Size:
        return Size(**data)


class CellSchema(Schema):
    pos = fields.Nested(PositionSchema)
    blocks = fields.List(fields.Nested(AbstractBlockSchema))


class MapSchema(Schema):
    map_size = fields.Nested(MapSizeSchema)
    cells = fields.List(fields.Nested(CellSchema))

    @post_load
    def make_map_size(self, data, **kwargs) -> GameMap:
        map = GameMap(data["map_size"])
        cell_data = data["cells"]
        for c in cell_data:
            for b in c["blocks"]:
                # Try to initialize it as a movable
                try:
                    b.initialize(pos=c["pos"], game_map=map)
                except AttributeError:
                    pass

                map.putBlock(c["pos"], b)
        return map

    @pre_dump
    def _pre_dump(self, map_obj: GameMap, **kwargs) -> Dict[str, Any]:
        cells_dicts = []
        for pos, cell in map_obj.blocks().items():
            if isinstance(cell.top(), EmptyBlock):
                continue
            cells_dicts.append({
                "pos": pos,
                "blocks": cell.data()
            })

        result = {
            "map_size": map_obj.size,
            "cells": cells_dicts,
        }
        return result
