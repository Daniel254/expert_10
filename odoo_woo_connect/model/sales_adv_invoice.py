# -*- coding: utf-8 -*-
#
#
#    Techspawn Solutions Pvt. Ltd.
#    Copyright (C) 2016-TODAY Techspawn(<http://www.Techspawn.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
import urllib2
import xmlrpclib
from collections import defaultdict
import base64
from odoo import models, fields, api, _

from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class sales_order_invoice(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    backend_id = fields.Many2many(comodel_name='wordpress.configure',
                                  string='Backend',
                                  store=True,
                                  readonly=False,
                                  required=False,
                                  )

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        data = super(sales_order_invoice, self)._create_invoice(
            order, so_line, amount)
        data.write(
            {'backend_id': [[6, 0, order.backend_id.ids]], 'sale_order_id': order.id})
        return data

    @api.multi
    def create_invoices(self):
        data = super(sales_order_invoice, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(
            self._context.get('active_ids', []))
        data['backend_id'] = [[6, 0, sale_orders.backend_id.ids]]
        data['sale_order_id'] = sale_orders.id

        return data
