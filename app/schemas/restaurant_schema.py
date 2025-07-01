from marshmallow import Schema, fields
from app.schemas.branch_schema import BranchSchema

class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    contact_number = fields.Str(required=True)
    description = fields.Str()
    branches = fields.List(fields.Nested(BranchSchema), dump_only=True)
