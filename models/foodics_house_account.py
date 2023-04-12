from odoo import fields, models, api


class FoodicsHouseAccount(models.Model):
    _name = 'foodics.house.account'
    _description = 'Foodics House Account'

    amount = fields.Char("Amount")
    old_balance = fields.Float("Old Balance")
    new_balance = fields.Float("New Balance")
    notes = fields.Text("Note")
