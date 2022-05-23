# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Terminal(models.Model):
    _name = "fuel.terminal"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Fuel transfer terminals detail"
    _order = 'name'
    _check_company_auto = True


    name = fields.Char(
        string='Display Name', 
        required=True, 
        copy=False, 
        index=True,
        tracking=True)

    terminal_num = fields.Char(
        string='Terminal No.', 
        required=True, 
        copy=False, 
        index=True,
        tracking=True)

    terminal_name = fields.Char(
        string='Terminal Name', 
        required=True, 
        copy=False, 
        index=True,
        tracking=True)
    
    address = fields.Char(tracking=True)
    city = fields.Char(tracking=True)
    state_id = fields.Many2one(
        "res.country.state", 
        string='State', 
        ondelete='restrict',
        tracking=True
    )
    zip = fields.Char(change_default=True)
    # country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    # partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    # partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
