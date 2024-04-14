from odoo import api, models, fields

class Customer(models.Model):
    _name = 'delivery.customer'
    _description = 'Customer'

    customer_id = fields.Char(string='Customer ID', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')

    orders = fields.One2many('delivery.order', 'customer_id', string='Orders')
    total_orders = fields.Integer(string='Total Orders', compute='_compute_total_orders')

    def _compute_total_orders(self):
        for customer in self:
            customer.total_orders = len(customer.orders)
    
    @api.model
    def create(self, vals):
        if vals.get('customer_id', 'New') == 'New':
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('delivery.customer_id') or 'New'
        return super(Customer, self).create(vals)