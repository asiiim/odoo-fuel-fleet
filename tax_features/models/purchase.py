# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    jurisdictions_id = fields.Many2many(
        'tax.jurisdiction',
        string='Destinations'
    )

    @api.onchange('jurisdictions_id')
    def update_taxes(self):
        if self.jurisdictions_id:
            for line in self.order_line:
                line.onchange_product_id()


    @api.onchange('partner_id')
    def get_destinations(self):
        if self.partner_id:
            self.jurisdictions_id = self.partner_id.jurisdictions_id
    

    has_orderline = fields.Boolean(compute='has_orderline', store=True)

    @api.depends('order_line')
    def has_orderline(self):
        for rec in self:
            if rec.order_line:
                rec.update({'has_orderline': True})


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    
    @api.onchange('product_id')
    def onchange_product_id(self):
        
        result = super(PurchaseOrderLine, self).onchange_product_id()
        
        if self.product_id:
            # take product categ
            categ = self.product_id.categ_id

            # take each jurisdiction selected in purchase order
            jurisdictions = self.order_id.jurisdictions_id
            
            # with those params lookup the tax tables
            taxes = self.env['account.tax'].search([
                ('type_tax_use', '=', 'purchase'),
                ('product_categ_id', '=', categ.id),
                ('jurisdiction_id', 'in', jurisdictions.ids)])

            self.taxes_id = taxes
        return result