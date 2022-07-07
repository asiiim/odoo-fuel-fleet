# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from collections import defaultdict
from odoo.exceptions import UserError

import json


class SaleOrder(models.Model):
    _inherit = "sale.order"

    terminal_id = fields.Many2one("fuel.terminal")

    # Update price of sales orderlines when changing those mentioned fields
    @api.onchange("commitment_date", "partner_id", "terminal_id")
    def update_price_unit(self):
        for line in self.order_line:
            line.product_uom_change()

    # Set terminal_id from sale to stock picking
    def _get_action_view_picking(self, pickings):
        result = super(SaleOrder, self)._get_action_view_picking(pickings)

        if pickings:
            for picking in pickings:
                if not picking.terminal_id:
                    picking.write({"terminal_id": self.terminal_id.id})
        return result


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # This method is called in other methods
    def get_price_unit(self):
        realtime_cost_records = self.env["product.realtime.cost"].search(
            [("date_time", "<=", self.order_id.commitment_date)], order="date_time desc"
        )

        cost_line = realtime_cost_records.mapped("cost_lines").filtered(
            lambda x: x.supplier_id == self.order_id.partner_id
            and x.terminal_id == self.order_id.terminal_id
            and x.product_id == self.product_id
        )

        if cost_line:
            return cost_line.mapped("cost")[0]
        else:
            return 0.0

    # Get unit price form realtime data on change of terminal, lift datetime,
    # supplier and product
    def product_uom_change(self):
        # Overriding the method --------
        result = super(SaleOrderLine, self).product_uom_change()

        if (
            self.product_id
            and self.order_id.partner_id
            and self.order_id.terminal_id
            and self.order_id.commitment_date
        ):

            cost = self.get_price_unit()
            self.price_unit = cost

        # Assign bol to each line from purchase order bol
        if self.product_id:
            self.bol_ref = self.order_id.bol_ref

        return
