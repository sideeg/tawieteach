from odoo import fields, models, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    foodics_id = fields.Char()