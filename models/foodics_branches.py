from odoo import fields, models, api


class FoodicsBranches(models.Model):
    _name = 'foodics.branches'
    _description = 'Foodics Branches'

    name = fields.Char("Name")
    latitude = fields.Float("Latitude")
    longitude = fields.Float("Longitude")
    reference = fields.Char("Reference")
    phone = fields.Char("Phone")
    open_from = fields.Char("Opening From")
    open_to = fields.Char("Opening To")
    inventory_end_of_day_time = fields.Char("Inventory End Of Day Time")
    receives_online_orders = fields.Boolean("Receives Online Orders")

