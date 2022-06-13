# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help='''Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal''')


    def button_validate(self):
        result = super(StockPicking, self).button_validate()

        for rec in self:
            purchase_rec = self.env['purchase.order'].search([('name', '=', rec.origin)])
            print('INFO Purchase Order Origin: ', purchase_rec.mapped('name'))
            purchase_orderlines = purchase_rec.mapped('order_line')

            if purchase_rec:
                for move in rec.move_ids_without_package:
                    filtered_pol = purchase_orderlines.filtered(lambda pol: pol.product_id == move.product_id)
                    print('Filtered POL: ', filtered_pol.mapped('product_id').mapped('name'))
                    if move.bol_ref in filtered_pol.mapped('bol_ref'):
                        continue
                    else:
                        raise UserError('Please check BOL of %s' % move.product_id.name)

        return result
