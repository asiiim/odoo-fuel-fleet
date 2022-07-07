# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    terminal_id = fields.Many2one("fuel.terminal")

    def action_make_new_quotation(self):
        po_form_view_id = self.env.ref("purchase.purchase_order_form").id
        return {
            "name": "Make New Quotation",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "view_id": po_form_view_id,
            "context": dict(
                self.env.context,
                default_requisition_id=self.id,
                default_user_id=False,
                default_terminal_id=self.terminal_id.id,
            ),
        }
