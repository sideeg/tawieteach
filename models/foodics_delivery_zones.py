from odoo import fields, models, api


class FoodicsDeliveryZones(models.Model):
    _name = 'foodics.delivery.zones'
    _description = 'Foodics Delivery Zones'

    name = fields.Char("Name")
    coordinates = fields.Char("Coordinates")
    reference = fields.Char("Reference")
