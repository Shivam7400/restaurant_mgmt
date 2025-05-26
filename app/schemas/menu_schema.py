from marshmallow import Schema, fields

class MenuSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category = fields.Str()
    restaurant_id = fields.Int(required=True)
