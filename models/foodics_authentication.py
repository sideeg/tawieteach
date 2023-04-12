# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FoodicsAuthentication(models.Model):
    _name = 'foodics.authentication'
    _description = 'Fooodics Authentication Info'

    name = fields.Char("Name", required=True)
    client_id = fields.Char("Client ID", required=True)
    client_secret = fields.Char("Client Secret", required=True)
    redirect_uri = fields.Char("Redirect Url", required=True)

