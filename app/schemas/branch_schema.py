from marshmallow import Schema, fields

class BranchSchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    restaurant_id = fields.Int(required=True)
