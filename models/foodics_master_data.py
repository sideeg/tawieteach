from odoo import fields, models, api

class ProductCategory (models.Model):
    _inherit = 'product.category'

    foodics_id = fields.Char()
    
class ProductsProduct(models.Model):
    _inherit = 'product.product'

    foodics_id = fields.Char()

class ProductCategory (models.Model):
    _inherit = 'pos.category'

    foodics_id = fields.Char()

class PaymentMethod (models.Model):
    _inherit = 'pos.payment.method'

    foodics_id = fields.Char()

class AccountTax(models.Model):
     _inherit = 'account.tax'

     foodics_id = fields.Char()

class AccountTaxGroup(models.Model):
     _inherit = 'account.tax.group'

     foodics_id = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    foodics_id = fields.Char()

class ResUsers(models.Model):
    _inherit = 'res.users'

    foodics_id = fields.Char()
