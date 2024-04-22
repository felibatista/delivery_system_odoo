from odoo import api, models, fields

class Product(models.Model):
    _name = 'delivery.product'
    _description = 'Product'

    product_id = fields.Char(string='Product ID', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))

    name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price', required=True)
    description = fields.Text(string='Description')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    order_line_ids = fields.One2many(
        comodel_name='delivery.order_line',
        inverse_name='product_id',
        string='Order Lines'
    )

    @api.model
    def create(self, vals):
        if vals.get('product_id', 'New') == 'New':
            vals['product_id'] = self.env['ir.sequence'].next_by_code('delivery.product_id') or 'New'
        return super(Product, self).create(vals)
    
    @api.constrains('price')
    def _check_price(self):
        for product in self:
            if product.price <= 0:
                raise models.ValidationError('Price must be greater than 0')
    
    def action_remove_product(self):
        for product in self:
            product.unlink()