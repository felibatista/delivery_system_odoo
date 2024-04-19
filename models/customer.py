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
    
    @api.constrains('phone')
    def _check_phone(self):
        for customer in self:
            if customer.phone and not customer.phone.isdigit():
                raise models.ValidationError('Phone must be a number')
        
    @api.constrains('email')
    def _check_email(self):
        for customer in self:
            if customer.email and '@' not in customer.email:
                raise models.ValidationError('Invalid email')
            
    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            self.email = self.email.lower()

    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone:
            self.phone = self.phone.replace(' ', '').replace('-', '')
    
    def action_view_orders(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'delivery.order',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
        }
        return action
            
    