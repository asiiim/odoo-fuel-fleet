# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class FuelAsset(models.Model):
    _name = "fuel.asset"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _description = "Fuel Asset Register"
    _order = "name"
    _check_company_auto = True

    name = fields.Char(
        string="Unique ID", required=True, copy=False, index=True, tracking=True
    )

    asset_name = fields.Char(string="Asset Name", copy=False, index=True, tracking=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "This Asset ID already exists !")
    ]
