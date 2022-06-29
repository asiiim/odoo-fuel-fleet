# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleInvoice(models.Model):
    _inherit = 'account.move'


    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help='''Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal''')
    driver_id = fields.Many2one('res.partner', domain="[('is_driver', '=', True)]")


    # Get total qty in the bottom section of the sales invoice.
    total_qty = fields.Char(
        string="Total Qty",
        compute='_get_total_qty',
        store=True)

    @api.depends('invoice_line_ids.quantity')
    def _get_total_qty(self):
        for invoice in self:
            qty = 0.0
            for line in invoice.invoice_line_ids:
                qty += line.quantity
            invoice.update({'total_qty': qty})
