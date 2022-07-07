# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    jurisdictions_id = fields.Many2many("tax.jurisdiction", string="Destinations")

    @api.onchange("jurisdictions_id")
    def update_taxes(self):
        if self.jurisdictions_id:
            for line in self.order_line:
                # Save the qty value before it gets
                # reset due to trigger of 'onchange_product_id()
                qty = line.product_qty
                line.onchange_product_id()
                line.product_qty = qty
        else:
            for line in self.order_line:
                line.taxes_id = None

    @api.onchange("partner_id")
    def get_destinations(self):
        if self.partner_id:
            self.jurisdictions_id = self.partner_id.jurisdictions_id

    # has_orderline = fields.Boolean(compute='has_orderline', store=True)

    # @api.depends('order_line')
    # def has_orderline(self):
    #     for rec in self:
    #         if rec.order_line:
    #             rec.update({'has_orderline': True})


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _onchange_quantity(self):

        result = super(PurchaseOrderLine, self)._onchange_quantity()

        if self.product_id:
            # take product categ
            categ = self.product_id.categ_id

            # take each jurisdiction selected in purchase order
            jurisdictions = self.order_id.jurisdictions_id

            # with those params lookup the tax tables
            taxes = self.env["account.tax"].search(
                [
                    ("type_tax_use", "=", "purchase"),
                    ("jurisdiction_id", "in", jurisdictions.ids),
                ]
            )

            print("Info: Selected taxes ", taxes.mapped("name"))

            # Add those taxes in the list
            taxes_list = []

            for tax in taxes:
                if categ in tax.product_categs_id:
                    taxes_list.append(tax)

            # Lookup each selected tax rate from the realtime tax rate model
            realtime_tax_rate_recs = self.env["realtime.tax.rate"].search(
                [("date_time", "<=", self.order_id.lift_datetime)],
                order="date_time desc",
            )

            print(
                "Info: Realtime Tax Rate Records: ",
                realtime_tax_rate_recs.mapped("name"),
            )

            if realtime_tax_rate_recs:
                for i, tax in enumerate(taxes_list):
                    rate_rec = realtime_tax_rate_recs.mapped("tax_lines").filtered(
                        lambda x: x.tax_id == tax
                    )

                    if rate_rec:
                        taxrate = rate_rec.mapped("rate")[0]
                        print("Info: Realtime Tax Rate of %s: %s" % (tax.name, taxrate))
                        taxes_list[i].write({"amount": taxrate})

            for tax in taxes_list:
                self.taxes_id += tax
        return
