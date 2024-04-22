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

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)


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
    
    @api.constrains('age')
    def _check_age(self):
        for carrier in self:
            if carrier.age < 18:
                raise models.ValidationError('Age must be greater than 18')
            
    @api.constrains('work_hours')
    def _check_work_hours(self):
        for carrier in self:
            if carrier.work_hours < 0:
                raise models.ValidationError('Work hours must be greater than 0')
            if carrier.work_hours > 8:
                raise models.ValidationError('Work hours must be less than 8')
        
    @api.constrains('phone')
    def _check_phone(self):
        for carrier in self:
            if carrier.phone and not carrier.phone.isdigit():
                raise models.ValidationError('Phone must be a number')
            
    def action_view_deliveries(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Deliveries',
            'res_model': 'delivery.order',
            'view_mode': 'tree,form',
            'domain': [('carrier_id', '=', self.id)],
        }
        return action
        
    def action_remove_carrier(self):
        for carrier in self:
            carrier.unlink()


