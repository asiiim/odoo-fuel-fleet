# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'


    # Feature of having Bill of Lading aks BOL# for each order line
    bol_ref = fields.Char('BOL#', help='Bill of Lading')