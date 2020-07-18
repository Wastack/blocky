from marshmallow import Schema, fields, post_load, validate
from marshmallow_oneofschema import OneOfSchema

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
    def make_position(self, data, **kwargs):
        return Position(**data)


class SpikeWallSchema(Schema):
    @post_load
    def make_spike(self, _data,  **kwargs):
        return KillerWall()

class AbstractWallSchema(OneOfSchema):
    type_schemas = {
        "Spike" : SpikeWallSchema,
    }

class PlayerSchema(Schema):
    pos = fields.Nested(PositionSchema)

    @post_load
    def make_player(self, data, **kwargs):
        return Player(), data["pos"]


class RockSchema(Schema):
    walls = fields.Dict(keys=fields.String(validate=validate.OneOf(["down", "up", "right", "left"])),
                        values=fields.Nested(AbstractWallSchema), required=False)
    pos = fields.Nested(PositionSchema)

    @post_load
    def make_map_size(self, data, **kwargs):
        if data.get("walls") is None:
            return RockBlock(), data["pos"]
        return RockBlock(walls=WallContainer(**data["walls"])), data["pos"]


class AbstractBlockSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {
        "Anna" : PlayerSchema,
        "Stone" : RockSchema,
    }

class MapSizeSchema(Schema):
    width = fields.Integer()
    height = fields.Integer()

    @post_load
    def make_map_size(self, data, **kwargs):
        return Size(**data)

class MapSchema(Schema):
    map_size = fields.Nested(MapSizeSchema())
    blocks = fields.List(fields.Nested(AbstractBlockSchema))

    @post_load
    def make_map_size(self, data, **kwargs):
        map = GameMap(data["map_size"])
        blocks = data["blocks"]
        for b, pos in blocks:
            map.putBlock(pos, b)
        return map
