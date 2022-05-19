# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'


    jurisdictions_id = fields.Many2many(
        'tax.jurisdiction',
        string='Destinations'
    )
        
