# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleInvoice(models.Model):
    _inherit = 'account.move'
