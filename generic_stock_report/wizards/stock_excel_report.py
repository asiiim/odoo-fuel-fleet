# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta


class StockProductCategoryReport(models.TransientModel):
    _name = "wizard.stock.excel.report"
    _description = "Stock Excel Report"

    start_date = fields.Date(
        string="Date From",
        required=True,
        default=lambda self: fields.Date.to_string(
            datetime.date.today().replace(day=1)
        ),
    )
    end_date = fields.Date(
        string="Date To",
        required=True,
        default=lambda self: fields.Date.to_string(
            (datetime.datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()
        ),
    )

    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        index=True,
        default=lambda self: self.env.user.company_id.id,
    )

    location_id = fields.Many2one(
        "stock.location",
        string="Locations",
        domain="[('usage','=','internal'),('company_id','=',company_id)]",
        required=True,
    )

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain="[('type', '=', 'product')]",
    )
    product_name = fields.Char(related="product_id.name")

    def print_report(self):
        context = self._context
        datas = {"ids": context.get("active_ids", [])}
        datas["model"] = "wizard.stock.excel.report"
        datas["form"] = self.read()[0]
        datas["location"] = self.location_id.display_name
        datas["product_id"] = self.product_id
        datas["product_name"] = self.product_name

        for field in datas["form"].keys():
            if isinstance(datas["form"][field], tuple):
                datas["form"][field] = datas["form"][field][0]
        return self.env.ref("generic_stock_report.stock_report_xlsx").report_action(
            self, data=datas
        )
