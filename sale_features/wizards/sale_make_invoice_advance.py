# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)

        invoice_vals.update({
            'driver_id': order.driver_id.id,
            'carrier_id': order.carrier_id.id,
            'bol_ref': order.bol_ref
        })

        print('Invoice Vals:::: ', invoice_vals)

        return invoice_vals

