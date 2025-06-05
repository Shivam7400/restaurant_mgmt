from marshmallow import Schema, fields

class ReservationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    table_id = fields.Int(required=True)
    reservation_time = fields.DateTime(required=True)
    guests_count = fields.Int(required=True)
    special_requests = fields.Str()
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
