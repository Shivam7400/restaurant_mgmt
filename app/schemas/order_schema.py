from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    item_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=True)
    total_price = fields.Float(dump_only=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    branch_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    order_items = fields.List(fields.Nested(OrderItemSchema), required=True)
