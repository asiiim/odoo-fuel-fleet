# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    terminal_id = fields.Many2one('fuel.terminal')
    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help="Carriers (trucking companies) approved to lift product from the specific Supplier at the specific Terminal")
    lift_datetime = fields.Datetime(
        string='Lift Date & Time', 
        required=True, 
        index=True, 
        copy=False,
        tracking=True, 
        default=fields.Datetime.now)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    net_gals = fields.Float('Net Gallons', 
        help='Volume of gallons temperature corrected to 60 degrees.')
    gross_gals = fields.Float('Gross Gallons',
        help='Volume of gallons at ambient temperature.')
    billed_gals = fields.Float('Billed Gallons', 
        help='Volume of gallons billed on invoice by Supplier.')
