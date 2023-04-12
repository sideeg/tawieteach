from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    foodics_id = fields.Char()


    # # change in compute tax
    # def _compute_amount_line_all(self):
    #     print('******************************************************************')
    #     self.ensure_one()
    #     fpos = self.order_id.fiscal_position_id
    #     tax_ids_after_fiscal_position = fpos.map_tax(self.tax_ids, self.product_id, self.order_id.partner_id)
    #     price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
    #     taxes = tax_ids_after_fiscal_position.compute_all(price, self.order_id.pricelist_id.currency_id, self.qty, product=self.product_id, partner=self.order_id.partner_id)
    #     if self.foodics_id :
    #         return {
    #         # 'price_subtotal_incl': taxes['total_included'],
    #         'price_subtotal': taxes['total_excluded'],
    #         }
    #     return {
    #         'price_subtotal_incl': taxes['total_included'],
    #         'price_subtotal': taxes['total_excluded'],
    #     }
