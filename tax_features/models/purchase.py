# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    jurisdictions_id = fields.Many2many(
        'tax.jurisdiction',
        string='Destinations'
    )

    @api.onchange('partner_id')
    def get_destinations(self):
        if self.partner_id:
            self.jurisdictions_id = self.partner_id.jurisdictions_id
    

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    
    @api.onchange('product_id')
    def onchange_product_id(self):
        
        result = super(PurchaseOrderLine, self).onchange_product_id()
        
        if self.product_id:
            # take product categ
            categ = self.product_id.categ_id
            print('Categ::::::', categ.name)

            # take each jurisdiction selected in purchase order
            jurisdictions = self.order_id.jurisdictions_id
            print('-----jurisdictions;;;;;;;;;', jurisdictions.ids)

            # with those params lookup the tax tables
            taxes = self.env['account.tax'].search([
                ('type_tax_use', '=', 'purchase'),
                ('product_categ_id', '=', categ.id),
                ('jurisdiction_id', 'in', jurisdictions.ids)])

            print('------Taxes:::::::', taxes.mapped('name'))

            self.taxes_id = taxes
        return result