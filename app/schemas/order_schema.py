from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    item_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    order_items = fields.List(fields.Nested(OrderItemSchema), required=True)
