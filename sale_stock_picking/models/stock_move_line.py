# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "picking_id" in vals and vals["picking_id"]:
                picking_rec = self.env["stock.picking"].browse(vals["picking_id"])

                if "location_id" in vals and vals["location_id"]:
                    if picking_rec.location_id.id != vals["location_id"]:
                        vals.update({"location_id": picking_rec.location_id.id})
                if "location_dest_id" in vals and vals["location_dest_id"]:
                    if picking_rec.location_dest_id.id != vals["location_dest_id"]:
                        vals.update(
                            {"location_dest_id": picking_rec.location_dest_id.id}
                        )

        res = super(StockMoveLine, self).create(vals_list)
        return res
