# -*- coding: utf-8 -*-
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


from odoo.tools import float_compare, float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Override this method to handle the pricelist item type of supplier_cost or
    # ref_index
    def price_compute(self, price_type, uom=False, currency=False, company=None):
        # compatibility about context keys used a bit everywhere in the code
        if not uom and self._context.get("uom"):
            uom = self.env["uom.uom"].browse(self._context["uom"])
        if not currency and self._context.get("currency"):
            currency = self.env["res.currency"].browse(self._context["currency"])

        products = self
        if price_type == "standard_price":
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            products = self.with_company(company or self.env.company).sudo()

        prices = dict.fromkeys(self.ids, 0.0)

        for product in products:
            # Add condition to overcome the error if price_type is supplier_cost or
            # index_ref
            if price_type in ["list_price", "standard_price"]:
                prices[product.id] = product[price_type] or 0.0
            elif price_type == "supplier_index":
                """
                - Get the realtime price
                - Set that price to the prices dict as prices[product.id]
                """
                prices[product.id] = 500

            if price_type == "list_price":
                prices[product.id] += product.price_extra
                # we need to add the price from the attributes that do not generate variants
                # (see field product.attribute create_variant)
                if self._context.get("no_variant_attributes_price_extra"):
                    # we have a list of price_extra that comes from the attribute values,
                    # we need to sum all that
                    prices[product.id] += sum(
                        self._context.get("no_variant_attributes_price_extra")
                    )

            if uom:
                prices[product.id] = product.uom_id._compute_price(
                    prices[product.id], uom
                )

            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                prices[product.id] = product.currency_id._convert(
                    prices[product.id],
                    currency,
                    product.company_id,
                    fields.Date.today(),
                )

        return prices
