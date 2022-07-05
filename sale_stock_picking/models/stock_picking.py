# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models



class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    
    @api.model
    def create(self, vals):
        if 'origin' in vals and vals['origin'] and vals['origin']:
            origin = vals['origin']
            if str(origin).startswith('S'):
                sales_rec = self.env['sale.order'].search([('name', '=', origin)], limit=1)
                if sales_rec:
                    vals.update({
                        'picking_type_id': sales_rec.picking_type_id.id, 
                        'location_id': sales_rec.picking_type_id.default_location_src_id.id, 
                        'location_dest_id': sales_rec.picking_type_id.default_location_dest_id.id,
                        'move_type': 'one'
                    })
        res = super(StockPicking, self).create(vals)
        return res
