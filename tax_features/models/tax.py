# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class TaxJurisdiction(models.Model):
    _name = "tax.jurisdiction"
    _description = "Tax Jurisdiction"
    _order = "name desc"
    _check_company_auto = True

    name = fields.Char(string="Jurisdiction")
    _sql_constraints = [
        (
            "check_duplicate_jurisdiction",
            "UNIQUE(name)",
            "This jurisdiction is already created !",
        ),
    ]


class AccountTax(models.Model):

    _inherit = "account.tax"

    jurisdiction_id = fields.Many2one(
        "tax.jurisdiction",
        string="Juridisction",
        tracking=True,
    )

    code = fields.Char(
        "Code",
        copy=False,
        tracking=True,
    )
    _sql_constraints = [
        ("check_duplicate_code", "UNIQUE(code)", "This code is already used !"),
    ]

    # product_categ_id = fields.Many2one('product.category', string="Product Category",
    # tracking=True,
    # help="Leave this field empty, if this tax is used as general")
    product_categs_id = fields.Many2many(
        "product.category",
        string="Product Category",
        tracking=True,
        help="Leave this field empty, if this tax is used as general",
    )
    tx_type = fields.Selection(
        selection=[("perunit", "Per Unit")],
        string="Type",
        required=True,
        tracking=True,
        default="perunit",
    )
    reflink = fields.Text(
        string="Reference",
        tracking=True,
    )
