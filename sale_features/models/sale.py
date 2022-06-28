# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help='''Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal''')
    driver_id = fields.Many2one('res.partner', domain="[('is_driver', '=', True)]")

    
    # Bill of lading
    bol_ref = fields.Char('BOL#', help='Bill of Lading', copy=False)


     # Set data from sale to stock picking
    def _get_action_view_picking(self, pickings):
        result = super(SaleOrder, self)._get_action_view_picking(pickings)

        if pickings:
            for picking in pickings:
                if not picking.driver_id:
                    picking.write({'driver_id': self.driver_id.id})
                if not picking.carrier_id:
                    picking.write({'carrier_id': self.carrier_id.id})
                if not picking.bol_ref:
                    picking.write({'bol_ref': self.bol_ref})
        return result



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    # Feature of having Bill of Lading aks BOL# for each order line
    bol_ref = fields.Char('BOL#', help='Bill of Lading', compute='get_bol', inverse='set_bol')

    @api.depends('order_id')
    def get_bol(self):
        for rec in self:
            if rec.order_id.bol_ref:
                rec.update({'bol_ref': rec.order_id.bol_ref})
    

    def set_bol(self):
        if self.bol_ref:
            self.order_id.update({'bol_ref': self.bol_ref})

