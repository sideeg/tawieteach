from odoo import fields, models, api


class DoodicsReasons(models.Model):
    _name = 'foodics.reasons'
    _description = ' Foodics Reason'

    name = fields.Char("Name")
