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
