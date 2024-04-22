from odoo import api, models, fields

class OrderLine(models.Model):
    _name = 'delivery.order_line'
    _description = 'Order Line'

    order_id = fields.Many2one('delivery.order', string='Order')
    product_id = fields.Many2one('delivery.product', string='Product')
    quantity = fields.Float(string='Quantity')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    @api.depends('quantity', 'product_id.price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.product_id.price

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise models.ValidationError('Quantity must be greater than 0')
    
    @api.constrains('product_id')
    def _check_product_id(self):
        for line in self:
            if not line.product_id:
                raise models.ValidationError('Product is required')
        
    @api.model
    def create(self, vals):
        if vals.get('order_id'):
            order = self.env['delivery.order'].browse(vals.get('order_id'))
            if order.status == 'done':
                raise models.UserError('Cannot add order line to done order')
        return super(OrderLine, self).create(vals)
    
    def write(self, vals):
        for line in self:
            if line.order_id.status == 'done':
                raise models.UserError('Cannot modify order line in done order')
        return super(OrderLine, self).write(vals)
    
    def action_remove_line(self):
        for line in self:
            line.unlink()