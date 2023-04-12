from odoo import fields, models, api


class FoodicsCharges(models.Model):
    _name = 'foodics.charges'
    _description = 'Foodics Charges'

    name = fields.Char("Name")
    name_localized = fields.Char("Name Localized")
    is_auto_applied = fields.Boolean("Auto Applied")
    value = fields.Char("Value")
    is_open_charge = fields.Boolean("Open Charge")
