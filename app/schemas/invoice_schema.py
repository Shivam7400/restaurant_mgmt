from marshmallow import Schema, fields

class InvoiceSchema(Schema):
    id = fields.Int(dump_only=True)
    invoice_number = fields.Str()
    order_id = fields.Int()
    issue_date = fields.DateTime()
    total_amount = fields.Float()
    payment_status = fields.Str()
