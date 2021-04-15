from dataclasses import asdict
from typing import List

from marshmallow import Schema, fields, post_load, pre_dump
from marshmallow_oneofschema import OneOfSchema

from game.json_import.map_schema import MapSchema, PositionSchema
from game.utils.MoveReports import MeltingIceReport, PlayerMoveReport, \
    MovableMoveReport, MoveReport


class MeltingIceReportSchema(Schema):
    life_was = fields.Integer()
    life_now = fields.Integer()
    position = fields.Nested(PositionSchema)

    @pre_dump
    def _pre_dump(self, report: MeltingIceReport, **_kwargs):
        return asdict(report)

    @post_load
    def post_load(self, data, **_kwargs) -> MeltingIceReport:
        return MeltingIceReport(**data)


class MovableMoveReportSchema(Schema):
    position = fields.Nested(PositionSchema)
    target = fields.Nested(PositionSchema)
    captured = fields.Boolean()

    @pre_dump
    def _pre_dump(self, report: MovableMoveReport, **_kwargs):
        return asdict(report)

    @post_load
    def post_load(self, data, **_kwargs) -> MovableMoveReport:
        return MovableMoveReport(**data)


class PlayerMoveReportSchema(Schema):
    died = fields.Boolean()
    position = fields.Nested(PositionSchema)

    @pre_dump
    def _pre_dump(self, report: PlayerMoveReport, **_kwargs):
        return asdict(report)

    @post_load
    def post_load(self, data, **_kwargs) -> PlayerMoveReport:
        return PlayerMoveReport(**data)


class MoveReportSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {
        "melting": MeltingIceReportSchema,
        "player": PlayerMoveReportSchema,
        "moving": MovableMoveReportSchema,
    }

    def get_obj_type(self, obj) -> str:
        obj_type = type(obj)
        if obj_type == MeltingIceReport:
            return "melting"
        elif obj_type == PlayerMoveReport:
            return "player"
        elif obj_type == MovableMoveReport:
            return "moving"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class StepSchema(Schema):
    reports = fields.List(fields.Nested(MoveReportSchema))

    @pre_dump
    def _pre_dump(self, reports: List[MoveReport], **_kwargs):
        return {"reports": reports}

    @post_load
    def post_load(self, data, **_kwargs) -> MovableMoveReport:
        return data["reports"]


class TurnSchema(Schema):
    steps = fields.List(fields.Nested(StepSchema))
    map_result = fields.Nested(MapSchema)