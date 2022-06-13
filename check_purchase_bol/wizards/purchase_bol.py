# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseBolWizard(models.TransientModel):
    _name = "purchase.bol.wizard"
    _description = "Wizard To Search Purchase by BOL"

    
    name = fields.Char('BOL#', help='Bill of Lading')


    def search_purchase_orders(self):
        '''
            - get purchase orderline records
            - search by bill of lading such that BOL value is in both upper and lower
        '''

        purchase_orderline_recs = self.env['purchase.order.line'].search([])
        filtered_recs = purchase_orderline_recs.filtered(
            lambda orderline: str(orderline.bol_ref).casefold() == str(self.name).casefold()).mapped('order_id')
        print('Info::: Searched Purchase Orders: ', filtered_recs.mapped('name'))
        return filtered_recs

    
    def action_view_purchases(self):
        purchases = self.search_purchase_orders()
        
        action = self.env['ir.actions.act_window']\
            ._for_xml_id('purchase.purchase_form_action')
        
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        
        elif len(purchases) == 1:
            res = self.env.ref('purchase.purchase_order_form', False)
            form_view = [(res and res.id or False, 'form')]

            if 'views' in action:
                action['views'] = form_view \
                    + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = purchases.id
        else:
            return {'type': 'ir.actions.act_window_close'}
        
        return action


