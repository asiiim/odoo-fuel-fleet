# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from collections import defaultdict
from odoo.exceptions import UserError

import json


class SaleOrder(models.Model):
    _inherit = "sale.order"

    carrier_id = fields.Many2one(
        "res.partner",
        domain="[('is_carrier', '=', True)]",
        help="""Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal""",
    )
    driver_id = fields.Many2one("res.partner", domain="[('is_driver', '=', True)]")

    # Bill of lading
    bol_ref = fields.Char("BOL#", help="Bill of Lading", copy=False)

    # Update driver and carrier value to created invoice
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        invoice_vals.update(
            {
                "driver_id": self.driver_id.id,
                "carrier_id": self.carrier_id.id,
            }
        )

        return invoice_vals

    # Set data from sale to stock picking
    def _get_action_view_picking(self, pickings):
        result = super(SaleOrder, self)._get_action_view_picking(pickings)

        if pickings:
            for picking in pickings:
                driver = carrier = bol = lift_datetime = None
                if not picking.driver_id:
                    driver = self.driver_id.id
                if not picking.carrier_id:
                    carrier = self.carrier_id.id
                if not picking.bol_ref:
                    bol = self.bol_ref
                if not picking.lift_datetime:
                    lift_datetime = self.commitment_date
                picking.write(
                    {
                        "driver_id": driver,
                        "carrier_id": carrier,
                        "bol_ref": bol,
                        "lift_datetime": lift_datetime,
                    }
                )
        return result

    # Get total qty in the bottom section of the sales order.
    total_qty = fields.Char(string="Total Qty", compute="_get_total_qty", store=True)

    @api.depends("order_line.product_uom_qty")
    def _get_total_qty(self):
        for order in self:
            qty = 0.0
            for line in order.order_line:
                qty += line.product_uom_qty
            order.update({"total_qty": qty})


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Feature of having Bill of Lading aks BOL# for each order line
    bol_ref = fields.Char(
        "BOL#", help="Bill of Lading", compute="get_bol", inverse="set_bol"
    )

    @api.depends("order_id")
    def get_bol(self):
        for rec in self:
            if rec.order_id.bol_ref:
                rec.update({"bol_ref": rec.order_id.bol_ref})

    def set_bol(self):
        if self.bol_ref:
            self.order_id.update({"bol_ref": self.bol_ref})

    # Add unique asset id for each line
    unique_asset_id = fields.Many2one("fuel.asset", string="Asset")
