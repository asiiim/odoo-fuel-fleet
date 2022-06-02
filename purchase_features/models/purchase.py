# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    terminal_id = fields.Many2one('fuel.terminal')
    carrier_id = fields.Many2one('res.partner', domain="[('is_carrier', '=', True)]",
        help="Carriers (trucking companies) approved to lift product from the specific Supplier at the specific Terminal")
    lift_datetime = fields.Datetime(
        string='Lift Date & Time', 
        required=True, 
        index=True, 
        copy=False,
        tracking=True, 
        default=fields.Datetime.now)

    
    @api.onchange('lift_datetime', 'partner_id', 'terminal_id')
    def update_price_unit(self):
        for line in self.order_line:
            line._onchange_quantity()
    


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    net_gals = fields.Float('Net Gallons', 
        help='Volume of gallons temperature corrected to 60 degrees.')
    gross_gals = fields.Float('Gross Gallons',
        help='Volume of gallons at ambient temperature.')
    billed_gals = fields.Float('Billed Gallons', 
        help='Volume of gallons billed on invoice by Supplier.')
    
    
    # -------------- View Realtime Cost------------------------------ #
    realtime_cost = fields.Many2one('product.realtime.cost',
    compute='get_realtime_cost', store=True)

    @api.depends('product_id', 
    'order_id.lift_datetime',
    'order_id.partner_id',
    'order_id.terminal_id')
    def get_realtime_cost(self):
        for rec in self:
            realtime_cost_records = self.env['product.realtime.cost'].search([
                ('date_time', '<=', self.order_id.lift_datetime)
            ], order='date_time desc')

            cost_line = realtime_cost_records.\
                mapped('cost_lines').filtered(
                lambda x: x.supplier_id == self.order_id.partner_id \
                    and x.terminal_id == self.order_id.terminal_id \
                    and x.product_id == self.product_id
            )
            
            if cost_line:
                rec.update({'realtime_cost': cost_line.mapped('realcost_id')[0].id})


    def action_view_realtime_cost(self):

        result = self.env["ir.actions.actions"]._for_xml_id('purchase_features.action_product_realtime_cost')
        
        result['context'] = {'default_realtime_cost': self.realtime_cost.id}
        
        res = self.env.ref('purchase_features.view_product_realtime_cost_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + [(state,view) for state,view in result['views'] if view != 'form']
        else:
            result['views'] = form_view
        result['target'] = 'new'
        result['res_id'] = self.realtime_cost.id
        
        return result

        # --------------------- End of View Realtime Cost -------------------- #

    
    # This method is called in other methods
    def get_price_unit(self):
        realtime_cost_records = self.env['product.realtime.cost'].search([
                ('date_time', '<=', self.order_id.lift_datetime)
            ], order='date_time desc')

        cost_line = realtime_cost_records.\
            mapped('cost_lines').filtered(
            lambda x: x.supplier_id == self.order_id.partner_id \
                and x.terminal_id == self.order_id.terminal_id \
                and x.product_id == self.product_id
        )

        if cost_line:
            return cost_line.mapped('cost')[0]
        else:
            return 0.0
        

    
    # Get unit price form realtime data on change of terminal, lift datetime,
    # supplier and product

    def _onchange_quantity(self):
        # Overriding the method --------
        result = super(PurchaseOrderLine, self)._onchange_quantity()
        
        if self.product_id and self.order_id.partner_id and \
            self.order_id.terminal_id and \
                self.order_id.lift_datetime:
            
            cost = self.get_price_unit()
            self.price_unit = cost

        return

