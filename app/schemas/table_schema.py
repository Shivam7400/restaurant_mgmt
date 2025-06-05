from marshmallow import Schema, fields

class TableSchema(Schema):
    id = fields.Int(dump_only=True)
    table_number = fields.Str(required=True)
    seats = fields.Int(required=True)
    is_available = fields.Bool(dump_only=True)
    location = fields.Str()
    branch_id = fields.Int(required=True)
