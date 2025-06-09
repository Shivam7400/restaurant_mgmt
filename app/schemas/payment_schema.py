from marshmallow import Schema, fields

class PaymentUpdateSchema(Schema):
    payment_status = fields.Str(required=True)
    payment_method = fields.Str(required=False)