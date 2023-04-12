from odoo import fields, models, api


class FoodicsDiscounts(models.Model):
    _name = 'foodics.discounts'
    _description = ' Foodics Discount'

    name = fields.Char("Name")
    amount = fields.Float("Amount")
    reference = fields.Char("Reference")
    minimum_product_price = fields.Float("Minimum Product Price")
    minimum_order_price = fields.Float("Minimum Order Price")
    maximum_amount = fields.Float("Maximum Amount")
    is_percentage = fields.Boolean("Is Percentage")
    is_taxable = fields.Boolean("Is Taxable")
