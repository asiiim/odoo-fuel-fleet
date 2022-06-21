# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    terminal_id = fields.Many2one('fuel.terminal')
    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help='''Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal''')
    lift_datetime = fields.Datetime(
        string='Lift Date & Time', 
        index=True, 
        copy=False,
        tracking=True)


    def button_validate(self):
        result = super(
            StockPicking, 
            self.with_context(skip_backorder=True, picking_ids_not_to_backorder=self.id))\
                .button_validate()

        return result

    
    # Bill of lading
    bol_ref = fields.Char('BOL#', help='Bill of Lading', copy=False)
