# -*- coding: utf-8 -*-

from itertools import chain

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_datetime
from odoo.tools.misc import formatLang, get_lang


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    # Added two extra options: supplier cost and index reference
    base = fields.Selection(
        [
            ("supplier_index", "Supplier Index"),
            ("list_price", "Sales Price"),
            ("standard_price", "Cost"),
            ("pricelist", "Other Pricelist"),
        ],
        "Based on",
        default="index_ref",
        required=True,
        help="Base price for computation.\n"
        "Supplier Cost: The base price will be the Supplier Realtime Cost.\n"
        "Index Reference: The base price will take reference from price of Realtime Cost.\n"
        "Sales Price: The base price will be the Sales Price.\n"
        "Cost Price : The base price will be the cost price.\n"
        "Other Pricelist : Computation of the base price based on another Pricelist.",
    )

    terminal_id = fields.Many2one("fuel.terminal")
    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
        change_default=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    # Location wise field
    partner_shipping_id = fields.Many2one(
        "res.partner",
        string="Location",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
