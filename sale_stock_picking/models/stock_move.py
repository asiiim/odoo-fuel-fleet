# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models



class StockMove(models.Model):
    _inherit = "stock.move"
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not 'picking_id' in vals:
                if 'sale_line_id' in vals and vals['sale_line_id']:
                    sale_order_rec = self.env['sale.order.line'].browse(vals['sale_line_id']).mapped('order_id')
                    picking_type_rec = sale_order_rec.mapped('picking_type_id')

                if 'location_id' in vals and vals['location_id']:
                    if picking_type_rec.default_location_src_id.id != vals['location_id']:
                        vals.update({'location_id': picking_type_rec.default_location_src_id.id})
                if 'location_dest_id' in vals and vals['location_dest_id']:
                    if picking_type_rec.default_location_dest_id.id != vals['location_dest_id']:
                        vals.update({'location_dest_id': picking_type_rec.default_location_dest_id.id})

        res = super(StockMove, self).create(vals_list)
        return res
