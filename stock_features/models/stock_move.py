# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'


    bol_ref = fields.Char('BOL#', help='Bill of Lading', compute='get_bol', inverse='set_bol')


    @api.depends('picking_id')
    def get_bol(self):
        for rec in self:
            if rec.picking_id.bol_ref:
                rec.update({'bol_ref': rec.picking_id.bol_ref})

    
    def set_bol(self):
        if self.bol_ref:
            self.picking_id.update({'bol_ref': self.bol_ref})


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    bol_ref = fields.Char('BOL#', related='move_id.bol_ref', store=True, readonly=True)
