# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class RealtimeTaxRate(models.Model):
    _name = "realtime.tax.rate"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Realtime Tax Rate Data"
    _order = 'name desc'
    _check_company_auto = True


    name = fields.Char(
        string='Reference', 
        required=True, 
        copy=False, 
        readonly=True, 
        index=True,
        tracking=True, 
        default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):

            vals['name'] = self.env['ir.sequence']\
                .next_by_code('realtime.tax.rate') or _('New')

        result = super(RealtimeTaxRate, self).create(vals)
        return result


    date_time = fields.Datetime(
        string='Date & Time', 
        required=True, 
        index=True, 
        copy=False,
        tracking=True, 
        default=fields.Datetime.now)

    tax_lines = fields.One2many('realtime.tax.rate.line', 'realtime_tax_rate_id',
        string='Rate Details', copy=True)


class RealtimeTaxRateLine(models.Model):
    _name = "realtime.tax.rate.line"
    _description = "Realtime Tax Rate Lines"
    _order = 'id desc'
    _check_company_auto = True


    realtime_tax_rate_id = fields.Many2one('realtime.tax.rate')
    
    tax_id = fields.Many2one(
        'account.tax',
        required=True
    )

    currency_id = fields.Many2one(
        'res.currency', 'Currency', 
        required=True,        
        default=lambda self: self.env.company.currency_id.id)

    rate = fields.Monetary(
        string='Rate',
        tracking=True,
        default=0.0)
