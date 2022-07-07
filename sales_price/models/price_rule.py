# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CustomerPriceRule(models.Model):
    _name = "customer.price.rule"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _description = "Customer Price Rule"
    _order = "name"
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

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "customer.price.rule"
            ) or _("New")

        result = super(CustomerPriceRule, self).create(vals)
        return result

    partner_id = fields.Many2one("res.partner", string="Customer")
    hierarchy = fields.Selection(
        [
            ("customer", "Customer Level"),
            ("product", "Product Level"),
            ("location", "Location Level"),
        ],
        string="Hierarchy",
        default="customer",
    )
    terminal_id = fields.Many2one("fuel.terminal")
    product_categ_id = fields.Many2one("product.category", string="Product Category")
    addtional_price = fields.Float("Addtional Price")
