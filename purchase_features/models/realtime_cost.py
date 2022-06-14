# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class ProductRealtimeCost(models.Model):
    _name = "product.realtime.cost"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Product Realtime Cost Data"
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
                .next_by_code('product.realtime.cost') or _('New')

        result = super(ProductRealtimeCost, self).create(vals)
        return result


    date_time = fields.Datetime(
        string='Date & Time', 
        required=True, 
        index=True, 
        copy=False,
        tracking=True, 
        default=fields.Datetime.now)

    cost_lines = fields.One2many('product.realtime.cost.line', 'realcost_id',
        string='Cost Details', copy=True)


class ProductRealtimeCostLine(models.Model):
    _name = "product.realtime.cost.line"
    _description = "Product Realtime Cost Data Details"
    _order = 'id desc'
    _check_company_auto = True


    realcost_id = fields.Many2one('product.realtime.cost')
    
    supplier_id = fields.Many2one(
        'res.partner', 
        string='Supplier', 
        required=True, 
        change_default=True, 
        tracking=True)

    terminal_id = fields.Many2one(
        'fuel.terminal', 
        string='Terminal', 
        required=True, 
        change_default=True, 
        tracking=True)

    product_id = fields.Many2one(
        'product.product', 
        string='Product', 
        domain=[('purchase_ok', '=', True)], 
        change_default=True,
        tracking=True)

    uom = fields.Many2one(related='product_id.uom_po_id', string='UoM',
        help='Unit of Measurement')

    currency_id = fields.Many2one(
        'res.currency', 'Currency', 
        required=True,        
        default=lambda self: self.env.company.currency_id.id)

    cost = fields.Float(string='Cost', required=True, digits=(16, 5), default=0.0)
