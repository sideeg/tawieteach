from odoo import fields, models, api


class FoodicsCombos(models.Model):
    _name = 'foodics.combos'
    _description = 'Foodics Combos'

    sku = fields.Char("SKU")
    barcode = fields.Char("Barcode")
    name = fields.Char("Name")
    name_localized = fields.Char("Name Localized")
    description = fields.Text("Description")
    description_localized = fields.Char("Description Localized")
    image = fields.Binary("Image")
    is_active = fields.Boolean("Active")
    is_ready = fields.Boolean("Ready")
