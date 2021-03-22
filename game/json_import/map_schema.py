import logging
from typing import Dict, Any

from marshmallow import Schema, fields, post_load, validate, pre_dump
from marshmallow_oneofschema import OneOfSchema

from game.blocks.impl.duck_pool import DuckPoolBlock
from game.blocks.impl.empty_block import EmptyBlock
from game.blocks.impl.melting_ice import MeltingIceBlock
from game.blocks.impl.player import Player
from game.blocks.impl.rock import RockBlock
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
        logging.debug("Killer wall is dumped")


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

    @post_load
    def make_player(self, data, **kwargs) -> Player:
        return Player()


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
        if data.get("walls") is None:
            return MeltingIceBlock(None, data["life"])
        return MeltingIceBlock(life=data["life"], walls=WallContainer(**data["walls"]))

    @pre_dump
    def _pre_dump(self, ice_block: MeltingIceBlock, **kwargs):
        walls_dict = ice_block.walls().walls()
        result = {}
        for direction, val in walls_dict.items():
            if val is None:
                continue
            result[direction.value] = val
        if not result:
            return {}
        return {"walls": result, "life": ice_block.life}


class DuckPoolSchema(Schema):
    capacity = fields.Integer()
    walls = fields.Dict(keys=fields.String(validate=validate.OneOf(["down", "up", "right", "left"])),
                        values=fields.Nested(AbstractWallSchema), required=False)

    @post_load
    def post_load(self, data, **kwargs) -> DuckPoolBlock:
        if data.get("walls") is None:
            return DuckPoolBlock(None, data["capacity"])
        return DuckPoolBlock(capacity=data["capacity"], walls=WallContainer(**data["walls"]))

    @pre_dump
    def _pre_dump(self, duck_pool_block: DuckPoolBlock, **kwargs):
        walls_dict = duck_pool_block.walls().walls()
        result = {}
        for direction, val in walls_dict.items():
            if val is None:
                continue
            result[direction.value] = val
        if not result:
            return {}
        return {"walls": result, "capacity": duck_pool_block.capacity}


class AbstractBlockSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {
        "Anna": PlayerSchema,
        "Stone": RockSchema,
        "MeltingIce": MeltingIceSchema,
        "DuckPool": DuckPoolSchema,
    }

    def get_obj_type(self, obj):
        # Order of isinstance is important: subclasses of more general classes
        # should be at front.
        if type(obj) == Player:
            return "Anna"
        elif type(obj) == MeltingIceBlock:
            return "MeltingIce"
        elif type(obj) == DuckPoolBlock:
            return "DuckPool"
        elif type(obj) == RockBlock:
            return "Stone"
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
                map.putBlock(c["pos"], b)
        return map

    @pre_dump
    def _pre_dump(self, map_obj: GameMap, **kwargs) -> Dict[str, Any]:
        logging.debug(map_obj)
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
