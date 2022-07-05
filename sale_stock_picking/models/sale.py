# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from collections import defaultdict
from odoo.exceptions import UserError

import json

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    READONLY_STATES = {
        'sale': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    @api.model
    def _default_picking_type(self):
        return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)

    
    @api.model
    def _get_picking_type(self, company_id):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return picking_type[:1]

    
    picking_type_id = fields.Many2one('stock.picking.type', 
        'Pick From', states=READONLY_STATES, required=True, 
        default=_default_picking_type, 
        domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
        help="This will determine operation type of outgoing shipment (delivery)")
