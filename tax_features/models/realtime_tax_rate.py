# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class RealtimeTaxRate(models.Model):
    _name = "realtime.tax.rate"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _description = "Realtime Tax Rate Data"
    _order = "name desc"
    _check_company_auto = True

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        tracking=True,
        default=lambda self: _("New"),
    )

    def _prepare_taxlines(self, tax_recs, realtime_tax_rate_id):
        vals_list = []
        for rec in tax_recs:
            vals_list.append(
                {
                    "tax_id": rec.id,
                    "rate": rec.amount,
                    "realtime_tax_rate_id": realtime_tax_rate_id,
                }
            )
        return vals_list

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):

            vals["name"] = self.env["ir.sequence"].next_by_code(
                "realtime.tax.rate"
            ) or _("New")

        result = super(RealtimeTaxRate, self).create(vals)

        # Add taxlines details as default value
        if not result.tax_lines:
            tax_recs = self.env["account.tax"].search([])
            realtime_taxrate_line_env = self.env["realtime.tax.rate.line"]
            tax_lines_vals = self._prepare_taxlines(tax_recs, result.id)
            for val in tax_lines_vals:
                realtime_taxrate_line_env.create(val)

        return result

    date_time = fields.Datetime(
        string="Date & Time",
        required=True,
        index=True,
        copy=False,
        tracking=True,
        default=fields.Datetime.now,
    )

    tax_lines = fields.One2many(
        "realtime.tax.rate.line",
        "realtime_tax_rate_id",
        string="Rate Details",
        copy=True,
    )


class RealtimeTaxRateLine(models.Model):
    _name = "realtime.tax.rate.line"
    _description = "Realtime Tax Rate Lines"
    _order = "id desc"
    _check_company_auto = True

    realtime_tax_rate_id = fields.Many2one("realtime.tax.rate")

    tax_id = fields.Many2one("account.tax", required=True)

    tax_type = fields.Selection(related="tax_id.type_tax_use")

    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    rate = fields.Float(required=True, digits=(16, 4), default=0.0)
