# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class VendorBill(models.Model):
    _inherit = 'account.move'


    bol_ref = fields.Char('BOL#', help='Bill of Lading')