# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    terminal_id = fields.Many2one("fuel.terminal")
    carrier_id = fields.Many2one(
        "res.partner",
        domain="[('is_carrier', '=', True)]",
        help="""Carriers (trucking companies) approved to lift product from the specific 
            Supplier at the specific Terminal""",
    )
    driver_id = fields.Many2one("res.partner", domain="[('is_driver', '=', True)]")
    lift_datetime = fields.Datetime(
        string="Lift Date & Time", index=True, copy=False, tracking=True
    )
    # date_planned = fields.Datetime(default=fields.Datetime.now)

    @api.onchange("lift_datetime", "partner_id", "terminal_id")
    def update_price_unit(self):
        for line in self.order_line:
            line._onchange_quantity()

        # Update receipt date
        if self.lift_datetime:
            self.update({"date_planned": self.lift_datetime})

    @api.onchange("date_planned")
    def check_set_receipt_date(self):
        if self.lift_datetime and self.date_planned:
            print("Info: Date Planned ", self.date_planned)
            print("Info: Lift Date and Time ", self.lift_datetime)
            if self.date_planned < self.lift_datetime:
                self.date_planned = self.lift_datetime

    # Set the bill date (invoice_date) default value with liftdate time
    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()

        invoice_vals.update(
            {
                "invoice_date": self.lift_datetime,
                # Add BOL to the Vendor Bill
                "bol_ref": self.bol_ref,
            }
        )

        return invoice_vals

    # Check the liftdatetime if set while confirming the RFQ into Purchase Order
    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()

        for rec in self:
            if not rec.lift_datetime:
                raise UserError(
                    "Please set Lift Date and Time of the RFQ: %s." % rec.name
                )
        return result

    # Set carrier data from purchase to stock picking
    def _prepare_picking(self):
        picking_vals = super(PurchaseOrder, self)._prepare_picking()

        if self.carrier_id:
            picking_vals.update(
                {
                    "carrier_id": self.carrier_id.id,
                    "bol_ref": self.bol_ref,
                    "terminal_id": self.terminal_id.id,
                    "driver_id": self.driver_id.id,
                    "lift_datetime": self.lift_datetime,
                }
            )

        return picking_vals

    # Bill of lading
    bol_ref = fields.Char("BOL#", help="Bill of Lading", copy=False)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # -------------- View Realtime Cost------------------------------ #
    realtime_cost = fields.Many2one(
        "product.realtime.cost", compute="get_realtime_cost", store=True
    )

    @api.depends(
        "product_id",
        "order_id.lift_datetime",
        "order_id.partner_id",
        "order_id.terminal_id",
    )
    def get_realtime_cost(self):
        for rec in self:
            realtime_cost_records = self.env["product.realtime.cost"].search(
                [("date_time", "<=", rec.order_id.lift_datetime)],
                order="date_time desc",
            )

            cost_line = realtime_cost_records.mapped("cost_lines").filtered(
                lambda x: x.supplier_id == rec.order_id.partner_id
                and x.terminal_id == rec.order_id.terminal_id
                and x.product_id == rec.product_id
            )

            if cost_line:
                rec.update({"realtime_cost": cost_line.mapped("realcost_id")[0].id})

    def action_view_realtime_cost(self):

        result = self.env["ir.actions.actions"]._for_xml_id(
            "purchase_features.action_product_realtime_cost"
        )

        result["context"] = {"default_realtime_cost": self.realtime_cost.id}

        res = self.env.ref("purchase_features.view_product_realtime_cost_form", False)
        form_view = [(res and res.id or False, "form")]
        if "views" in result:
            result["views"] = form_view + [
                (state, view) for state, view in result["views"] if view != "form"
            ]
        else:
            result["views"] = form_view
        result["target"] = "new"
        result["res_id"] = self.realtime_cost.id

        return result

        # --------------------- End of View Realtime Cost -------------------- #

    # This method is called in other methods
    def get_price_unit(self):
        realtime_cost_records = self.env["product.realtime.cost"].search(
            [("date_time", "<=", self.order_id.lift_datetime)], order="date_time desc"
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
    def _onchange_quantity(self):
        # Overriding the method --------
        result = super(PurchaseOrderLine, self)._onchange_quantity()

        if (
            self.product_id
            and self.order_id.partner_id
            and self.order_id.terminal_id
            and self.order_id.lift_datetime
        ):

            cost = self.get_price_unit()
            self.price_unit = cost

        # Assign bol to each line from purchase order bol
        if self.product_id:
            self.bol_ref = self.order_id.bol_ref

        return

    # This method is overriden to set default value for date planned
    @api.onchange("product_id")
    def set_date_planned(self):
        self.date_planned = self.order_id.lift_datetime

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
