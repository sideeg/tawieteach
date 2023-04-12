from odoo import fields, models, api


class FoodicsUsers(models.Model):
    _name = 'foodics.users'
    _description = ' Foodics User'

    name = fields.Char("Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    pin = fields.Char("PIN")





