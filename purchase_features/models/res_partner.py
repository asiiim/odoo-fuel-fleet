# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_carrier = fields.Boolean(string='Is Carrier?', default=False)

    @api.onchange('is_carrier')
    def set_company(self):
        for rec in self:
            if rec.is_carrier:
                rec.update({'company_type': 'company'})
        