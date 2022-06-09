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
                ('jurisdiction_id', 'in', jurisdictions.ids)])

            # Add those taxes in the list
            taxes_list = []
            
            for tax in taxes:
                if categ in tax.product_categs_id:
                    taxes_list.append(tax)


            # Lookup each selected tax rate from the realtime tax rate model
            realtime_tax_rate_recs = self.env['realtime.tax.rate'].search([
                ('date_time', '<=', self.order_id.lift_datetime)
            ], order='date_time desc')

            if realtime_tax_rate_recs:
                for i, tax in enumerate(taxes_list):
                    rate_rec = realtime_tax_rate_recs.\
                        mapped('tax_lines').filtered(
                        lambda x: x.tax_id == tax
                    )

                    if rate_rec:
                        taxrate = rate_rec.mapped('rate')[0]
                        taxes_list[i].write({'amount': taxrate})
            
            for tax in taxes_list:
                self.taxes_id += tax
        return result