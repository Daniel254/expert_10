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

from odoo import models, api, fields, _
from api import API
from odoo.exceptions import Warning

from ..unit.backend_adapter import WpImportExport


class wp_configure(models.Model):

    """ Models for wordpress configuration """
    _name = "wordpress.configure"
    _description = 'WooCommerce Backend Configuration'

    name = fields.Char(string='name')
    location = fields.Char("Url")

    consumer_key = fields.Char("Consumer key")
    consumer_secret = fields.Char("Consumer Secret")
    version = fields.Selection([('v1', 'v1')], 'Version')
    verify_ssl = fields.Boolean("Verify SSL")

    @api.multi
    def test_connection(self):
        """ Test connection with the given url """
        location = self.location
        cons_key = self.consumer_key
        sec_key = self.consumer_secret
        version = "wc/v1"
        wcapi = API(url=location, consumer_key=cons_key,
                    consumer_secret=sec_key, version=version, wp_api=True)
        r = wcapi.get("products")
        if r.status_code == 404:
            raise Warning(_("Enter Valid url"))
        msg = ''
        if r.status_code != 200:
            msg = r.json()['message'] + '\n Error Code ' + \
                str(r.json()['data']['status'])
            raise Warning(_(msg))
        else:
            raise Warning(_('Test Success'))
        return True

    @api.multi
    def map_products(self):
        """ Assign backend to all the products """
        all_products = self.env['product.template'].search(
            [('backend_id', '!=', self.id)])
        for product in all_products:
            backends = []
            for backend_id in product.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            product.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_product_tags(self):
        """ Assign backend to all the products categories """
        all_tags = self.env['product.product.tag'].search(
            [('backend_id', '!=', self.id)])
        for tag in all_tags:
            backends = []
            for backend_id in tag.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            tag.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_taxes(self):
        """ Assign backend to all the taxes """
        all_taxes = self.env['account.tax'].search(
            [('backend_id', '!=', self.id)])
        for tax in all_taxes:
            backends = []
            for backend_id in tax.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            tax.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_attributes(self):
        """ Assign backend to all the product attributes """
        all_attributes = self.env['product.attribute'].search(
            [('backend_id', '!=', self.id)])
        for attribute in all_attributes:
            backends = []
            for backend_id in attribute.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            attribute.write({'backend_id': [[6, False, backends]]})
        self.map_attribute_values()
        return True

    @api.multi
    def map_attribute_values(self):
        """ Assign backend to all the products attribute values """
        all_att_values = self.env['product.attribute.value'].search(
            [('backend_id', '!=', self.id)])
        for attr_value in all_att_values:
            backends = []
            for backend_id in attr_value.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            attr_value.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_categories(self):
        """ Assign backend to all the products categories """
        all_categories = self.env['product.category'].search(
            [('backend_id', '!=', self.id)])
        for category in all_categories:
            backends = []
            for backend_id in category.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            category.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_customers(self):
        """ Assign backend to all the customers """
        all_customers = self.env['res.partner'].search(
            [('backend_id', '!=', self.id)])
        for customer in all_customers:
            backends = []
            for backend_id in customer.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            customer.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def map_sale_order(self):
        """ Assign backend to all the sales orders """
        all_sale_orders = self.env['sale.order'].search(
            [('backend_id', '!=', self.id)])
        for sale_order in all_sale_orders:
            backends = []
            for backend_id in sale_order.backend_id:
                backends.append(backend_id.id)
            if not self.id in backends:
                backends.append(self.id)
            sale_order.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_products(self):
        """ Remove particular backend from all the products """
        all_products = self.env['product.template'].search(
            [('backend_id', '=', self.id)])
        for product in all_products:
            backends = []
            for backend_id in product.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            product.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_product_tags(self):
        """ Remove particular backend from all the product tags """
        all_tags = self.env['product.product.tag'].search(
            [('backend_id', '=', self.id)])
        for tag in all_tags:
            backends = []
            for backend_id in tag.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            tag.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_taxes(self):
        """ Remove particular backend from all the taxes """
        all_taxes = self.env['account.tax'].search(
            [('backend_id', '=', self.id)])
        for tax in all_taxes:
            backends = []
            for backend_id in tax.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            tax.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_attributes(self):
        """ Remove particular backend from all the products attributes """
        all_attributes = self.env['product.attribute'].search(
            [('backend_id', '=', self.id)])
        for attribute in all_attributes:
            backends = []
            for backend_id in attribute.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            attribute.write({'backend_id': [[6, False, backends]]})
        self.unmap_attribute_values()
        return True

    @api.multi
    def unmap_attribute_values(self):
        """ Remove particular backend from all products attribute values """
        all_att_values = self.env['product.attribute.value'].search(
            [('backend_id', '=', self.id)])
        for attr_value in all_att_values:
            backends = []
            for backend_id in attr_value.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            attr_value.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_categories(self):
        """ Remove particular backend from all the categories """
        all_categories = self.env['product.category'].search(
            [('backend_id', '=', self.id)])
        for category in all_categories:
            backends = []
            for backend_id in category.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            category.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_customers(self):
        """ Remove particular backend from all the customers """
        all_customers = self.env['res.partner'].search(
            [('backend_id', '=', self.id)])
        for customer in all_customers:
            backends = []
            for backend_id in customer.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            customer.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def unmap_sale_order(self):
        """ Remove particular backend from all the sales orders """
        all_sale_orders = self.env['sale.order'].search(
            [('backend_id', '=', self.id)])
        for sale_order in all_sale_orders:
            backends = []
            for backend_id in sale_order.backend_id:
                if self.id != backend_id.id:
                    backends.append(backend_id.id)
            sale_order.write({'backend_id': [[6, False, backends]]})
        return True

    @api.multi
    def export_products(self):
        """ Export all the products of particular backend """

        all_products = self.env['product.template'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for product in all_products:
            product.export_product(self)
        return True

    @api.multi
    def export_taxes(self):
        """ Export all the products of particular backend """

        all_taxes = self.env['account.tax'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for tag in all_taxes:
            tag.export_tax(self, 'standard')
        return True

    @api.multi
    def export_product_tags(self):
        """ Export all the products of particular backend """

        all_product_tags = self.env['product.product.tag'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for tag in all_product_tags:
            tag.export_product_tag(self)
        return True

    @api.multi
    def export_categories(self):
        """ Export all the products of categories backend """
        all_categories = self.env['product.category'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for category in all_categories:
            category.export_product_category(self)
        return True

    @api.multi
    def export_attributes(self):
        """ Export all the products attributes of particular backend """
        all_attributes = self.env['product.attribute'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for attribute in all_attributes:
            attribute.export_product_attribute(self)
            for value in attribute.value_ids:
                value.export_product_attribute_value(self)
        return True

    @api.multi
    def export_customers(self):
        """ Export all the customers of particular backend """
        all_customers = self.env['res.partner'].search(
            [('backend_id', '=', self.id), ('customer', '=', True)])
        export = WpImportExport(self)
        for customer in all_customers:
            customer.export_customer(self)
        return True

    @api.multi
    def export_sale_order(self):
        """ Export all the sales orders of particular backend """
        all_sales_orders = self.env['sale.order'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for sales_order in all_sales_orders:
            sales_order.export_sales_order(self)
        return True

    @api.multi
    def export_invoices_refund(self):
        """ Export all the refund invoice orders of particular backend """
        all_invoice_orders = self.env['account.invoice'].search(
            [('backend_id', '=', self.id)])
        export = WpImportExport(self)
        for account_invoice in all_invoice_orders:
            account_invoice.export_invoice_refund(self)
        return True
