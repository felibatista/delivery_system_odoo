from odoo import api, fields, models

class DeliveryCarrier(models.Model):
    _name = 'delivery.carrier'
    _description = 'Carrier'

    carrier_id = fields.Char(string='Carrier ID', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', default=18)
    work_hours = fields.Float(string='Work Hours', default=8.0)
    active = fields.Boolean(string='Active', default=True)
    phone = fields.Char(string='Phone')

    delivery_ids = fields.One2many('delivery.order', 'carrier_id', string='Deliveries')
    total_deliveries = fields.Integer(string='Total Deliveries', compute='_compute_total_deliveries')
    total_money = fields.Float(string='Total Money', compute='_compute_total_money')

    def _compute_total_deliveries(self):
        for carrier in self:
            carrier.total_deliveries = len(carrier.delivery_ids)
    
    def _compute_total_money(self):
        for carrier in self:
            carrier.total_money = sum(order.amount for order in carrier.delivery_ids)

    @api.model
    def create(self, vals):
        if vals.get('carrier_id', 'New') == 'New':
            vals['carrier_id'] = self.env['ir.sequence'].next_by_code('delivery.carrier_id') or 'New'
        return super(DeliveryCarrier, self).create(vals)
        


