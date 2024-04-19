from odoo import api, models, fields

class Order(models.Model):
    _name = 'delivery.order'
    _description = 'Order'

    order_id = fields.Char(string='Order ID', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    name = fields.Char(string='Order Name', required=True)
    customer_id = fields.Many2one('delivery.customer', string='Customer', required=True)
    date = fields.Date(string='Order Date', default=fields.Date.today())
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    amount = fields.Float(string='Amount')

    @api.model
    def create(self, vals):
        if vals.get('order_id', 'New') == 'New':
            vals['order_id'] = self.env['ir.sequence'].next_by_code('delivery.order_id') or 'New'
        return super(Order, self).create(vals)
    
    @api.constrains('amount')
    def _check_amount(self):
        for order in self:
            if order.amount < 0:
                raise models.ValidationError('Amount must be greater than 0')
            
    @api.constrains('status')
    def _check_status(self):
        for order in self:
            if order.status == 'done' and order.amount == 0:
                raise models.ValidationError('Amount must be greater than 0 for done status')
    
    def action_end_delivery(self):
        for order in self:
            if order.status == 'done':
                raise models.ValidationError('Order is already done')
            order.status = 'done'



    
